from logging import getLogger

from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session
from src.api_parsers.dblp import DblpParser
from src.api_parsers.scopus import ScopusParser
from src.auth import is_authorized
from src.auth.core import get_user_id
from src.common.models import SearchTaskStatus
from src.common.postgres import get_db_session
from src.models.author import Source
from src.search.models import (
    DetailsResponseModel,
    FilenameResponseModel,
    HistoryEntity,
    HistoryResponseModel,
    Keywords,
    SearchTaskCreationResponseModel,
    StatusResponseModel,
    SuggestionsResponseModel,
)
from src.search.repositories import AuthorRepository, SearchRepository
from src.worker import celery

router = APIRouter()
logger = getLogger(__name__)


@router.get("/", status_code=200, dependencies=[Depends(is_authorized)])
async def root() -> dict:
    return {"greeting": "hello"}


@router.post("/search/file", status_code=200)
async def create_search_task(
    file: UploadFile,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
) -> SearchTaskCreationResponseModel:
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid document type.")
    try:
        file_contents = file.file.read()
        search = SearchRepository.create_search(
            db_session=db_session,
            user_id=user_id,
            file_name=file.filename,
        )
        task_result = celery.send_task("search", (file_contents, search.id))
        SearchRepository.update(db_session, search, {"task_id": task_result.id})
    except Exception:
        raise HTTPException(500, detail="Internal server error.")
    return SearchTaskCreationResponseModel(filename=file.filename)


@router.post("/search/keywords/{search_id}", status_code=200)
async def search_by_keywords(
    keywords: Keywords,
    search_id: int,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
) -> SearchTaskCreationResponseModel:
    search = SearchRepository.find_by_id(db_session, search_id)
    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")
    if search is None or search.status != SearchTaskStatus.READY:
        raise HTTPException(404, detail="Page not found.")
    try:
        SearchRepository.update(db_session, search, {"keywords": keywords})
        task_result = celery.send_task(
            "search_by_keywords", (search.keywords, search.abstract, search.id)
        )
        SearchRepository.update(db_session, search, {"task_id": task_result.id})
    except Exception:
        raise HTTPException(500, detail="Internal server error.")
    return SearchTaskCreationResponseModel(filename=search.file_name)


@router.get("/search/{search_id}/status", status_code=200)
async def get_search_status(
    search_id: int,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
):
    search = SearchRepository.find_by_id(db_session, search_id)

    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    task_status = AsyncResult(search.task_id).status
    if (
        search.status != SearchTaskStatus.PENDING
        or task_status in states.UNREADY_STATES
    ):
        return StatusResponseModel(status=search.status)

    if task_status in states.EXCEPTION_STATES:
        search = SearchRepository.update(
            db_session, search, {"status": SearchTaskStatus.ERROR}
        )
    elif task_status == states.SUCCESS:
        search = SearchRepository.update(
            db_session, search, {"status": SearchTaskStatus.READY}
        )
    return StatusResponseModel(status=search.status)


@router.get(
    "/search/{search_id}/results",
    status_code=200,
)
async def get_results(
    search_id: int,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
) -> SuggestionsResponseModel:
    search = SearchRepository.find_by_id(db_session, search_id)

    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    if search is None or search.status != SearchTaskStatus.READY:
        raise HTTPException(404, detail="Page not found.")

    all_venues = []
    authors = AuthorRepository.find_all_by_value(db_session, "search_id", search_id)
    authors = sorted(
        authors, key=lambda a: a.publication.similarity_score, reverse=True
    )

    for author in authors:
        if author.publication.venues:
            all_venues.extend(author.publication.venues)

    return SuggestionsResponseModel(authors=authors, venues=set(all_venues))


@router.get("/search/history", status_code=200)
async def get_history(
    request: Request,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
) -> HistoryResponseModel:
    results = []
    history = SearchRepository.find_all_by_value(
        db_session, "user_id", user_id, order_by_field="id", desc=True
    )
    for search_index, search in enumerate(history):
        results.append(
            HistoryEntity(
                id=search.id,
                index=search_index,
                filename=search.file_name,
                status=search.status,
            )
        )
    return results


@router.get(
    "/search/source/{source}/author/{author_id}/details",
    status_code=200,
)
async def get_author_details(
    source: Source,
    author_id: str,
    session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
):
    author = AuthorRepository.find_first_by_value(
        session=session, lookup_field="id", lookup_value=author_id
    )

    search = SearchRepository.find_first_by_value(
        session=session, lookup_field="id", lookup_value=author.search_id
    )

    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    if author is None:
        raise HTTPException(404, detail="No such author found in the database.")

    affiliation = author.affiliation

    if not affiliation:
        if source == Source.DBLP:
            dblp_parser = DblpParser()
            affiliation = dblp_parser.get_author_affiliation(
                author_name=f"{author.first_name} {author.last_name}",
                author_id=author.author_external_id,
            )
        elif source == Source.Scopus:
            scopus_parser = ScopusParser()
            affiliation = scopus_parser.get_author_affiliation(
                author_id=author.author_external_id
            )
    if affiliation and affiliation != author.affiliation:
        update_data = {"affiliation": affiliation}
        AuthorRepository.update(
            session=session, instance=author, update_data=update_data
        )
    return DetailsResponseModel(affiliation=affiliation)


@router.get(
    "/search/{search_id}/filename",
    status_code=200,
    dependencies=[Depends(is_authorized)],
)
async def get_filename(
    search_id: int,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
) -> FilenameResponseModel:
    search = SearchRepository.find_by_id(db_session, lookup_id=search_id)

    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    return search


@router.delete("/search/{search_id}", status_code=200)
async def delete_search(
    search_id: int,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
):
    search = SearchRepository.find_by_id(session=db_session, lookup_id=search_id)

    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    if not search:
        raise HTTPException(
            status_code=404, detail=f"Search with id {search_id} does not exist."
        )

    task = AsyncResult(search.task_id)
    if task.status in states.UNREADY_STATES:
        logger.info(f"Terminating pending task {search.task_id}")
        task.revoke(terminate=True)
    SearchRepository.delete(session=db_session, instance=search)
    return {"info": f"Deleted search with id {search_id}"}


@router.get("/search/{search_id}/keywords")
async def get_keywords(
    search_id: int,
    db_session: Session = Depends(get_db_session),
    user_id=Depends(get_user_id),
):
    search = SearchRepository.find_by_id(session=db_session, lookup_id=search_id)

    if search.user_id != user_id:
        raise HTTPException(403, "Forbidden")

    if not search:
        raise HTTPException(
            status_code=404, detail=f"Search with id {search_id} does not exist."
        )

    return {"keywords": search.keywords}
