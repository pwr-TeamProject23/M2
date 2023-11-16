from src.api_parsers.exceptions import NoAuthorsException
from src.api_handlers.scopus.handler import ScopusHandler
from src.api_parsers.models import Source, Publication, Author
from requests.exceptions import HTTPError
import json


class ScopusParser:
    def __init__(self, keywords: str):
        self.keywords = keywords
        self.handler = ScopusHandler()

    def _get_author_affiliation(self, author_id: str) -> str:
        params = {"view": "ENHANCED"}
        author_response = self.handler.get_author_by_id(
            author_id=author_id, params=params
        )
        affiliation = _extract_affiliation(author_response)
        return affiliation

    def get_authors(self) -> list[Author]:
        pub_params = {
            "query": f"TITLE-ABS-KEY({self.keywords})",
            "view": "COMPLETE",
        }
        try:
            pub_response = self.handler.get_abstracts_and_citations(params=pub_params)
        except HTTPError:
            raise NoAuthorsException(self.keywords)
        authors: list[Author] = []
        for page in pub_response:
            if "error" in page:
                raise NoAuthorsException(self.keywords)
            page_authors = self._parse_publications_page(page)
            authors.extend(page_authors)
        return authors

    def _parse_entry_dict(self, entry: dict) -> list[Author]:
        authors: list[Author] = []
        pub_data = {
            "title": entry["dc:title"],
            "abstract": entry.get("dc:description"),
            "citations": entry.get("citedby-count"),
            "year": entry["prism:coverDate"].split("-")[0],
            "source_api": Source.SCOPUS,
        }
        publication = Publication(**pub_data)
        if "author" not in entry:
            return []
        authors_list = entry["author"]
        for author in authors_list:
            first_name = author.get("given-name")
            last_name = author.get("surname")
            if first_name is None and last_name is None:
                continue
            author_id = author["authid"]
            auth_data = {
                "first_name": first_name,
                "last_name": last_name,
                "api_id": author_id,
                "publication": publication,
                "affiliation": self._get_author_affiliation(author_id=author_id),
            }
            authors.append(Author(**auth_data))
        return authors

    def _parse_publications_page(self, page: dict) -> list[Author]:
        authors: list[Author] = []
        entries = page["search-results"]["entry"]
        for entry in entries:
            authors.extend(self._parse_entry_dict(entry))
        return authors


def _extract_affiliation(author_response: dict) -> str:
    profile = author_response["author-retrieval-response"][0]["author-profile"]
    affiliation = profile["affiliation-current"]["affiliation"]
    if type(affiliation) == list:
        return affiliation[0]["ip-doc"]["afdispname"]
    return affiliation["ip-doc"]["afdispname"]
