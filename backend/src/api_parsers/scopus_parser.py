from src.api_parsers.exceptions import NoAuthorsException, MaxAuthorsReachedException
from src.api_handlers.scopus.handler import ScopusHandler
from src.api_parsers.models import Source, Publication, Author
from src.similarity_eval.similarity_eval import SimilarityEvaluator
from requests.exceptions import HTTPError


class ScopusParser:
    def __init__(
        self, keywords: str, abstract: str, min_year: int = 2010, max_authors: int = 100
    ):
        self.keywords = keywords
        self.abstract = abstract
        self.handler = ScopusHandler()
        self.authors = []
        self.min_year = min_year
        self.max_authors = max_authors

    def get_author_affiliation(self, author_id: str) -> str:
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
        for page in pub_response:
            if "error" in page:
                raise NoAuthorsException(self.keywords)
            try:
                self._parse_publications_page(page)
            except MaxAuthorsReachedException:
                break
        sim_eval = SimilarityEvaluator(self.abstract)
        self.authors = sim_eval.update_author_similarities(self.authors)
        return self.authors

    def _parse_entry_dict(self, entry: dict) -> None:
        year = int(entry["prism:coverDate"].split("-")[0])
        if year < self.min_year:
            return
        pub_data = {
            "doi": entry.get("prism:doi"),
            "title": entry["dc:title"],
            "year": year,
            "venues": None,
            "abstract": entry.get("dc:description"),
            "citation_count": entry.get("citedby-count"),
            "similarity_score": 0,
        }
        publication = Publication(**pub_data)
        if "author" not in entry:
            return
        authors_list = entry["author"]
        for author in authors_list:
            first_name = author.get("given-name")
            last_name = author.get("surname")
            if first_name is None and last_name is None:
                continue
            if first_name is None:
                first_name = last_name
                last_name = ""
            author_id = author["authid"]
            auth_data = {
                "author_external_id": author_id,
                "first_name": first_name,
                "last_name": last_name,
                "affiliation": None,
                "email": None,
                "source": Source.Scopus,
                "publication": publication,
            }
            author = Author(**auth_data)
            self.authors.append(author)
            if len(self.authors) >= self.max_authors:
                raise MaxAuthorsReachedException()

    def _parse_publications_page(self, page: dict) -> None:
        entries = page["search-results"]["entry"]
        for entry in entries:
            self._parse_entry_dict(entry)


def _extract_affiliation(author_response: dict) -> str | None:
    profile = author_response["author-retrieval-response"][0]["author-profile"]
    affiliation = profile["affiliation-current"]["affiliation"]
    if type(affiliation) == list:
        return affiliation[0]["ip-doc"]["afdispname"]
    return affiliation["ip-doc"]["afdispname"]
