from sqlalchemy.orm import Session
from src.common.models import SearchTaskStatus
from src.common.repository import BaseRepository
from src.models.author import Author, Source
from src.models.publication import Publication
from src.models.search import Search


class AuthorRepository(BaseRepository[Author]):
    __model__ = Author

    @classmethod
    def create_author(
        cls,
        db_session: Session,
        search_id: int,
        author_external_id: str,
        first_name: str,
        last_name: str,
        affiliation: str,
        email: str,
        source: Source,
    ) -> Author:
        author = Author(
            search_id=search_id,
            author_external_id=author_external_id,
            first_name=first_name,
            last_name=last_name,
            affiliation=affiliation,
            email=email,
            source=source,
        )
        return cls.create(db_session, author)


class SearchRepository(BaseRepository[Search]):
    __model__ = Search

    @classmethod
    def create_search(
        cls,
        db_session: Session,
        user_id: int,
        file_name: str,
        task_id: str | None = None,
        status: SearchTaskStatus = SearchTaskStatus.PENDING,
    ) -> Search:
        search = Search(
            user_id=user_id, file_name=file_name, task_id=task_id, status=status
        )
        return cls.create(db_session, search)


class PublicationRepository(BaseRepository[Publication]):
    __model__ = Publication

    @classmethod
    def create_publication(
        cls,
        db_session: Session,
        author_id: int,
        doi: str,
        title: str,
        year: int,
        venue: str | None = None,
        citation_count: int | None = None,
        abstract: str | None = None,
    ):
        publication = Publication(
            author_id=author_id,
            doi=doi,
            title=title,
            year=year,
            venue=venue,
            citation_count=citation_count,
            abstract=abstract,
        )
        cls.create(db_session, publication)
