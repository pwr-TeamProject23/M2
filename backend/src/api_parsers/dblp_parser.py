from requests.exceptions import HTTPError
from src.api_handlers.dblp.handler import DblpHandler
from src.api_handlers.core.exceptions import QuotaExceededException
from src.api_parsers.models import Source, Publication, Author
from src.api_parsers.exceptions import (
    NoAuthorsException,
    NoAffiliationException,
    DBLPQuotaExceededException,
    MaxAuthorsReachedException,
)


class DBLPParser:
    def __init__(self, keywords: str, min_year: int = 2010, max_authors: int = 10):
        self.keywords = keywords
        self.handler = DblpHandler()
        self.authors = []
        self.min_year = min_year
        self.max_authors = max_authors

    def get_authors(self) -> list[Author]:
        try:
            pub_response = self.handler.get_publications(self.keywords)
            for page in pub_response:
                self._parse_publications_page(page)
        except (DBLPQuotaExceededException, MaxAuthorsReachedException):
            return self.authors
        except (HTTPError, QuotaExceededException):
            raise NoAuthorsException(self.keywords)
        return self.authors

    def _parse_publications_page(self, page: dict) -> None:
        hits = page["result"]["hits"]["hit"]
        for hit in hits:
            self._parse_hit_dict(hit)

    def _parse_hit_dict(self, hit: dict) -> None:
        info = hit["info"]
        year = info["year"]
        if int(year) < self.min_year:
            return
        pub_data = {
            "title": info["title"],
            "abstract": "",
            "citations": 0,
            "year": year,
            "source_api": Source.DBLP,
        }
        publication = Publication(**pub_data)
        authors_list = info["authors"]["author"]
        if type(authors_list) == dict:
            authors_list = [authors_list]
        for author in authors_list:
            author_id = author["@pid"]
            author_name = author["text"]
            split_name = author_name.split()
            first_name, last_name = split_name[0], " ".join(split_name[1:])
            try:
                affiliation = self._get_author_affiliation(
                    author_name=author_name, author_id=author_id
                )
            except QuotaExceededException:
                raise DBLPQuotaExceededException()
            except NoAffiliationException:
                continue
            auth_data = {
                "first_name": first_name,
                "last_name": last_name,
                "api_id": author_id,
                "publication": publication,
                "affiliation": affiliation,
            }
            self.authors.append(Author(**auth_data))
            if len(self.authors) >= self.max_authors:
                raise MaxAuthorsReachedException()

    def _get_author_affiliation(self, author_name: str, author_id: str) -> str:
        author_response = self.handler.get_authors(author_name)
        for page in author_response:
            affiliation = _extract_affiliation(author_id, page)
            if affiliation is not None:
                return affiliation
        raise NoAffiliationException(author_id=author_id)


def _extract_affiliation(author_id: str, page: dict) -> str | None:
    results = page["result"]["hits"]["hit"]
    for hit in results:
        info = hit["info"]
        if not info["url"].endswith(author_id):
            continue
        if info.get("notes") is None:
            raise NoAffiliationException(author_id=author_id)
        notes = info["notes"]["note"]
        if type(notes) != list:
            if notes["@type"] == "affiliation":
                return notes["text"]
            raise NoAffiliationException(author_id=author_id)
        for note in notes:
            if note["@type"] == "affiliation":
                return note["text"]
        raise NoAffiliationException(author_id=author_id)
    return None
