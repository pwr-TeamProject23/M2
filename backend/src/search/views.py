from logging import getLogger

from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from src.auth import is_authorized
from src.api_parsers.dblp import DblpParser
from src.api_parsers.scopus import ScopusParser
from src.common.models import SearchTaskStatus
from src.common.postgres import get_db_session
from src.models.author import Source
from src.search.models import (
    DetailsResponseModel,
    FilenameResponseModel,
    HistoryEntity,
    HistoryResponseModel,
    SearchTaskCreationResponseModel,
    StatusResponseModel,
    SuggestionsResponseModel,
)
from src.search.repositories import AuthorRepository, SearchRepository, PublicationRepository
from src.worker import celery

router = APIRouter()
logger = getLogger(__name__)


@router.get("/", status_code=200, dependencies=[Depends(is_authorized)])
async def root() -> dict:
    return {"greeting": "hello"}


@router.post(
    "/search/file/{user_id}", status_code=200, dependencies=[Depends(is_authorized)]
)
async def create_search_task(
    file: UploadFile, user_id: int, db_session: Session = Depends(get_db_session)
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


@router.get(
    "/search/{search_id}/status", status_code=200, dependencies=[Depends(is_authorized)]
)
async def get_search_status(
    search_id: int, db_session: Session = Depends(get_db_session)
):
    try:
        search = SearchRepository.find_by_id(db_session, search_id)
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
    except Exception:
        raise HTTPException(500, detail="Internal server error.")


@router.get(
    "/search/{search_id}/results",
    status_code=200,
    dependencies=[Depends(is_authorized)],
)
async def get_results(
    search_id: int, db_session: Session = Depends(get_db_session)
) -> SuggestionsResponseModel:
    search = SearchRepository.find_by_id(db_session, search_id)
    if search is None or search.status != SearchTaskStatus.READY:
        raise HTTPException(404, detail="Page not found.")
    all_venues = []
    authors = AuthorRepository.find_all_by_value(db_session, "search_id", search_id)
    authors = sorted(authors, key=lambda a: a.publication.similarity_score, reverse=True)
    for author in authors:
        if author.publication.venues:
            all_venues.extend(author.publication.venues)
    return SuggestionsResponseModel(authors=authors, venues=set(all_venues))


@router.get(
    "/search/history/{user_id}", status_code=200, dependencies=[Depends(is_authorized)]
)
async def get_history(
    user_id: int, db_session: Session = Depends(get_db_session)
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
    dependencies=[Depends(is_authorized)],
)
async def get_author_details(
    source: Source,
    author_id: str,
    session: Session = Depends(get_db_session),
):
    author = AuthorRepository.find_first_by_value(
        session=session, lookup_field="id", lookup_value=author_id
    )
    if author is None:
        raise HTTPException(400, detail="No such author found in the database.")
    affiliation = author.affiliation
    if not affiliation:
        parser = (
            DblpParser()
            if source == Source.DBLP
            else ScopusParser()
            if source == Source.Scopus
            else None
        )
        if parser:
            affiliation = parser.get_author_affiliation(
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
    search_id: int, db_session: Session = Depends(get_db_session)
) -> FilenameResponseModel:
    return SearchRepository.find_by_id(db_session, lookup_id=search_id)


@router.delete("/search/{search_id}", status_code=200, dependencies=[Depends(is_authorized)])
async def delete_search(
    search_id: int,  db_session: Session = Depends(get_db_session)
):
    try:
        search = SearchRepository.find_by_id(session=db_session, lookup_id=search_id)
        authors = AuthorRepository.find_all_by_value(session=db_session, lookup_field="search_id", lookup_value=search_id)
        publications = []
        for author in authors:
            publications.extend(PublicationRepository.find_all_by_value(session=db_session, lookup_field="author_id", lookup_value=author.id))
    except:
        raise HTTPException(
            400,
            detail="Search with given id does not exist",
        )

    task_id = search.task_id
    task = AsyncResult(task_id)
    
    if task.status.lower() == SearchTaskStatus.PENDING:
        logger.info("Terminating pending task {}".format(task_id))
        task.revoke(terminate=True)
    
    for publication in publications:
        PublicationRepository.delete(session=db_session, instance=publication)
    
    for author in authors:
        AuthorRepository.delete(session=db_session, instance=author)

    SearchRepository.delete(session=db_session, instance=search)
    
    return {"info": f"deleted search with id {search_id}"}
   