from io import BytesIO
from logging import getLogger

from src.api_parsers.dblp_parser import DBLPParser
from src.api_parsers.exceptions import NoAuthorsException
from src.api_parsers.scopus_parser import ScopusParser
from src.articles_service.articles_parser import ArticleParser, KeywordParsingError
from src.common.postgres import SessionLocal
from src.models.author import Author
from src.models.publication import Publication
from src.search.repositories import AuthorRepository, PublicationRepository
from src.worker.core import celery

logger = getLogger(__name__)


@celery.task(name="search", bind=True)
def search(self, file_contents: bytes, search_id: int) -> None:
    try:
        db_session = SessionLocal()
        article_parser = ArticleParser(BytesIO(file_contents))
        abstract = article_parser.get_abstract()
        keywords = article_parser.get_keywords()
        search_results = []

        for keyword in keywords[0]:
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

        for keyword in keywords[1]:
            parser = DBLPParser(keywords=keyword.replace("\n", " "))
            try:
                dblp_results = [
                    (author, author.publication) for author in parser.get_authors()
                ]
            except NoAuthorsException:
                continue
            search_results.extend(dblp_results)

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
    except KeywordParsingError:
        logger.error("Failed to parse keywords from article")
        raise
    except Exception:
        logger.error("Encountered exception during search task")
        raise
