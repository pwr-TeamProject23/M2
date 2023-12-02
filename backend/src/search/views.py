from typing import BinaryIO

from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from src.auth import is_authorized
from src.common.models import SearchTaskStatus
from src.models.author import Source
from src.search.models import (
    DetailsResponseModel,
    HistoryResponseModel,
    StatusResponseModel,
    SuggestionsResponseModel,
)
from src.search.repositories import SearchRepository

router = APIRouter()


@router.get("/", dependencies=[Depends(is_authorized)])
async def root() -> dict:
    return {"greeting": "hello"}


@router.post(
    "/search/file/{user_id}", status_code=200, dependencies=[Depends(is_authorized)]
)
async def create_search_task(file: UploadFile, user_id: int) -> dict:
    if file.content_type != "application/pdf":
        raise HTTPException(400, detail="Invalid document type.")

    try:
        file_content: BinaryIO = file.file
    except Exception:
        raise HTTPException(500, detail="Internal server error.")

    return {"message": "successful upload", "filename": file.filename}


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
async def get_results(search_id: int) -> SuggestionsResponseModel:
    result = [
        {
            "id": 1,
            "name": "Wolfram Fenske",
            "src": "DBLP",
            "year": 2015,
            "title": "When code smells twice as much: Metric-based detection of variability-aware code smells.",
            "venues": ["International Conference on Software Engineering (ICSE)"],
        },
        {
            "id": 2,
            "name": "Yang Zhang",
            "src": "Scopus",
            "year": 2023,
            "title": "MIRROR: multi-objective refactoring recommendation via correlation analysis",
            "venues": None,
        },
        {
            "id": 3,
            "name": "Francesca Arcelli Fontana",
            "src": "Google Scholar",
            "year": 2012,
            "title": "Evaluating the lifespan of code smells using software repository mining",
            "venues": ["IEEE/ACM International Conference on Software Engineering (ICSE)"],
        },
        {
            "id": 4,
            "name": "Francesca Arcelli Fontana",
            "src": "Google Scholar",
            "year": 2014,
            "title": "Evaluating the lifespan of code smells using software repository mining",
            "venues": ["IEEE/ACM International Conference on Software Engineering (ICSE)", "Venue2"],
        },
        {
            "id": 5,
            "name": "John Doe",
            "src": "Scopus",
            "year": 2022,
            "title": "Exploring the Future of Software Development",
            "venues": None,
        },
    ]
    
    venues = []
    
    for author in result:
        author_venues = author.get("venues")
        
        if author_venues == None:
            continue
        
        for venue in author_venues:
            venues.append(venue)

    return SuggestionsResponseModel(
        authors=result,
        venues=set(
            venues
        ),
    )


@router.get(
    "/search/history/{user_id}", status_code=200, dependencies=[Depends(is_authorized)]
)
async def get_history(user_id: int) -> HistoryResponseModel:
    return [
        {
            "id": 1,
            "index": 0,
            "filename": "article about machine learning",
            "status": SearchTaskStatus.PENDING,
        },
        {
            "id": 5,
            "index": 1,
            "filename": "article about cloud computing",
            "status": SearchTaskStatus.READY,
        },
        {
            "id": 3,
            "index": 2,
            "filename": "article about something else",
            "status": SearchTaskStatus.ERROR,
        },
    ]


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
