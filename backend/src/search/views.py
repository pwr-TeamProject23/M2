from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from logging import getLogger
from src.auth import is_authorized
from src.common.models import SearchTaskStatus
from src.common.postgres import get_db_session
from src.models.author import Source, Author
from src.search.models import (
    AuthorResponseModel,
    DetailsResponseModel,
    HistoryEntity,
    HistoryResponseModel,
    PublicationResponseModel,
    SearchTaskCreationResponseModel,
    StatusResponseModel,
    SuggestionsResponseModel,
)
from src.search.repositories import (
    AuthorRepository,
    PublicationRepository,
    SearchRepository,
)
from src.api_parsers.scopus_parser import ScopusParser
from src.api_parsers.dblp_parser import DBLPParser
from src.api_parsers.exceptions import (
    NoAffiliationException,
    DBLPQuotaExceededException,
)
from src.worker import celery

router = APIRouter()
logger = getLogger(__name__)


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
    results, all_venues = [], []
    authors = AuthorRepository.find_all_by_value(db_session, "search_id", search_id)
    for author in authors:
        publication = PublicationRepository.find_first_by_value(
            db_session, "author_id", author.id
        )
        results.append(
            AuthorResponseModel(
                id=author.id,
                firstName=author.first_name,
                lastName=author.last_name,
                email=author.email,
                source=author.source,
                publication=PublicationResponseModel(
                    doi=publication.doi,
                    title=publication.title,
                    year=publication.year,
                    venues=publication.venues,
                    abstract=publication.abstract,
                    citationCount=publication.citation_count,
                    similarityScore=publication.similarity_score
                )
            )
        )
        if publication.venues:
            all_venues.extend(publication.venues)
    return SuggestionsResponseModel(
        authors=results,
        venues=set(all_venues),
    )


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
    "/search/{search_id}/source/{source}/author/{author_id}/details",
    status_code=200,
    dependencies=[Depends(is_authorized)],
)
async def get_author_details(
    search_id: int,
    source: Source,
    author_id: str,
    session: Session = Depends(get_db_session),
):
    instance: Author = AuthorRepository.find_first_by_value(session=session, lookup_field="id", lookup_value=author_id)
    if instance is None:
        raise HTTPException(
            400,
            detail="No such author found in the database.",
        )
    author_external_id = instance.author_external_id

    if source == Source.DBLP:
        dblp_parser = DBLPParser("")
        author_first_name = instance.first_name
        author_last_name = instance.last_name
        author_name = " ".join([author_first_name, author_last_name])
        try:
            affiliation = dblp_parser.get_author_affiliation(
                author_id=author_external_id, author_name=author_name
            )
        except NoAffiliationException:
            logger.error(f"No affiliation for author_id {author_id}.", exc_info=False)
            raise HTTPException(
                500,
                detail="This author is associated with no affiliation that exists in DBLP.",
            )
        except DBLPQuotaExceededException:
            raise HTTPException(500, detail="DBLP quota exceeded.")
    elif source == Source.Scopus:
        scopus_parser = ScopusParser("", "")
        affiliation = scopus_parser.get_author_affiliation(author_id=author_external_id)
    else:
        raise HTTPException(
            400,
            detail="Invalid source. Affiliation requests are available only for DBLP and Scopus.",
        )

    update_data = {"affiliation": affiliation}
    AuthorRepository.update(session=session, instance=instance, update_data=update_data)
    return DetailsResponseModel(affiliation=affiliation)
