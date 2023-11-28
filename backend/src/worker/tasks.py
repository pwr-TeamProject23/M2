from io import BytesIO

from src.api_parsers.dblp_parser import DBLPParser
from src.api_parsers.exceptions import NoAuthorsException
from src.api_parsers.scopus_parser import ScopusParser
from src.articles_service.articles_parser import ArticleParser
from src.common.postgres import get_db_session
from src.models.author import Author
from src.search.repositories import AuthorRepository
from src.worker.core import celery


@celery.task(name="search", bind=True)
def search(self, file_contents: bytes, search_id: int) -> None:
    db_session = get_db_session()
    article_parser = ArticleParser(BytesIO(file_contents))
    keywords = article_parser.get_keywords()
    authors = []

    for keyword in keywords[0]:
        parser = ScopusParser(keywords=keyword.replace("\n", " "))
        try:
            scopus_authors = parser.get_authors()
        except NoAuthorsException:
            continue
        authors.extend(scopus_authors)

    for keyword in keywords[1]:
        parser = DBLPParser(keywords=keyword.replace("\n", " "))
        try:
            dblp_authors = parser.get_authors()
        except NoAuthorsException:
            continue
        authors.extend(dblp_authors)

    authors = [
        Author(search_id=search_id, **author.model_dump()) for author in authors
    ]
    AuthorRepository.create_all(db_session, authors)

