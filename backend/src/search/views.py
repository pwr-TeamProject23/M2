from typing import BinaryIO

from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from src.auth import is_authorized
from src.common.models import SearchTaskStatus
from src.common.postgres import get_db_session
from src.models.author import Source
from src.search.models import (
    AuthorResponseModel,
    DetailsResponseModel,
    HistoryEntity,
    HistoryResponseModel,
    StatusResponseModel,
    SearchTaskCreationResponseModel,
    SearchTaskStatusResponseModel,
    StatusResponseModel,
    SuggestionsResponseModel,
)
from src.search.repositories import SearchRepository
from src.search.repositories import (
    AuthorRepository,
    PublicationRepository,
    SearchRepository,
)
from src.worker import celery

router = APIRouter()


@router.get("/", dependencies=[Depends(is_authorized)])
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


@router.get("/search/{search_id}/status")
async def get_search_status(search_id: int, db_session: Session):
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
    results = []
    authors = AuthorRepository.find_all_by_value(db_session, "search_id", search_id)
    for author in authors:
        publication = PublicationRepository.find_first_by_value(
            db_session, "author_id", author.id
        )
        results.append(
            AuthorResponseModel(
                id=author.id,
                name=f"{author.first_name} {author.last_name}",
                src=author.source,
                year=publication.year if publication else None,
                title=publication.title if publication else None,
                affiliation=author.affiliation,
                venue=publication.venue if publication else None,
            )
        )
    return SuggestionsResponseModel(
        authors=results,
        venues=set([author.venue for author in results if author.venue is not None]),
    )


@router.get(
    "/search/history/{user_id}", status_code=200, dependencies=[Depends(is_authorized)]
)
async def get_history(
    user_id: int, db_session: Session = Depends(get_db_session)
) -> HistoryResponseModel:
    results = []
    history = SearchRepository.find_all_by_value(db_session, "user_id", user_id)
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
    "/search/{search_id}/source/{source}/author/{author_id}/details",
    status_code=200,
    dependencies=[Depends(is_authorized)],
)
async def get_author_details(search_id: int, source: Source, author_id: int):
    affiliation = {
        1: "Otto von Guericke University of Magdeburg, Germany",
        2: "Hebei University of Science and Technology",
        3: "Università degli Studi di Milano-Bicocca",
        4: "PWr",
        5: "Example University",
    }.get(author_id)

    return DetailsResponseModel(affiliation=affiliation)
