from io import BytesIO
from logging import getLogger

from src.api_parsers.dblp_parser import DBLPParser
from src.api_parsers.exceptions import NoAuthorsException
from src.api_parsers.scopus_parser import ScopusParser
from src.api_parsers.scholar_parser import ScholarParser
from src.articles_service.articles_parser import ArticleParser
from src.common.models import SearchTaskStatus
from src.common.postgres import SessionLocal
from src.models.author import Author
from src.models.publication import Publication
from src.search.repositories import (
    AuthorRepository,
    PublicationRepository,
    SearchRepository,
)
from src.similarity_eval.similarity_eval import scale_scores
from src.worker.core import celery

logger = getLogger(__name__)


@celery.task(name="search", bind=True)
def search(self, file_contents: bytes, search_id: int) -> None:
    db_session = SessionLocal()
    try:
        article_parser = ArticleParser(BytesIO(file_contents))
        abstract = article_parser.get_abstract()
        keywords = article_parser.get_keywords()
        search_results = []

        for keyword in keywords:
            parser = ScopusParser(
                keywords=keyword.replace("\n", " "), abstract=abstract
            )
            try:
                scopus_results = [
                    (author, author.publication) for author in parser.get_authors()
                ]
            except NoAuthorsException:
                continue
            search_results.extend(scopus_results)

        for keyword in keywords:
            parser = DBLPParser(keywords=keyword.replace("\n", " "))
            try:
                dblp_results = [
                    (author, author.publication) for author in parser.get_authors()
                ]
            except NoAuthorsException:
                continue
            search_results.extend(dblp_results)

        for keyword in keywords:
            parser = ScholarParser(keywords=keyword.replace("\n", " "), abstract=abstract, max_authors=15)
            try:
                scholar_results = [
                    (author, author.publication) for author in parser.get_authors()
                ]
            except NoAuthorsException:
                continue
            search_results.extend(scholar_results)

        search_results = scale_scores(search_results)

        authors, publications = [], []
        for author, publication in search_results:
            author = author.model_dump()
            author.pop("publication")
            author = Author(search_id=search_id, **author)
            publication = Publication(author=author, **publication.model_dump())
            authors.append(author)
            publications.append(publication)

        AuthorRepository.create_all(db_session, authors)
        PublicationRepository.create_all(db_session, publications)
        db_session.close()
    except Exception as exc:
        logger.error(
            f"Encountered exception during search task, details: {exc}", exc_info=True
        )
        failed_search = SearchRepository.find_by_id(db_session, search_id)
        SearchRepository.update(
            db_session, failed_search, {"status": SearchTaskStatus.ERROR}
        )
        raise
