from io import BytesIO
from logging import getLogger

from src.api_parsers.core.models import ParsedAuthor
from src.api_parsers.dblp import DblpParser
from src.api_parsers.scholar import ScholarParser
from src.api_parsers.scopus import ScopusParser
from src.articles_service.articles_parser import ArticleParser
from src.common.models import SearchTaskStatus
from src.common.postgres import SessionLocal
from src.models.author import Author
from src.models.publication import Publication
from src.search.repositories import AuthorRepository, SearchRepository
from src.similarity_eval.similarity_eval import SimilarityEvaluator, scale_scores
from src.worker.core import celery

logger = getLogger(__name__)


@celery.task(name="search", bind=True)
def search(self, file_contents: bytes, search_id: int) -> None:
    db_session = SessionLocal()
    try:
        logger.error("Starting search for {}".format(search_id))
        article_parser = ArticleParser(BytesIO(file_contents))
        abstract = article_parser.get_abstract()
        keywords = article_parser.get_keywords()
        found_authors: list[ParsedAuthor] = []
        logger.error("Finished parsing PDF for {}".format(search_id))

        scopus_parser = ScopusParser()
        scopus_authors = scopus_parser.get_authors_and_publications(keywords=keywords)
        found_authors.extend(scopus_authors)

        dblp_parser = DblpParser()
        dblp_authors = dblp_parser.get_authors_and_publications(keywords=keywords)
        found_authors.extend(dblp_authors)

        scholar_parser = ScholarParser()
        scholar_authors = scholar_parser.get_authors_and_publications(keywords=keywords)
        found_authors.extend(scholar_authors)

        if abstract:
            similarity_evaluator = SimilarityEvaluator()
            similarity_evaluator.update_author_similarities(abstract, found_authors)
            scale_scores(found_authors)

        authors = []
        for found_author in found_authors:
            author_dict = found_author.model_dump()
            publication_dict = author_dict.pop("publication")
            author = Author(search_id=search_id, **author_dict)
            author.publication = Publication(author=author, **publication_dict)
            authors.append(author)

        AuthorRepository.create_all(db_session, authors)
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
