from collections.abc import Iterator
from logging import getLogger

from pydantic import ValidationError
from requests import HTTPError
from src.api_handlers.scopus import ScopusHandler
from src.api_parsers.core.models import ParsedAuthor, ParsedPublication, Source
from src.api_parsers.scopus.queries import GET_PUBLICATION_BY_MIN_PUBYEAR_AND_KEYWORDS
from src.config import SCOPUS_SEARCH_MAX_PAGES, SCOPUS_SEARCH_MIN_PUBYEAR


class ScopusParser:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.scopus_handler = ScopusHandler()

    def get_authors_and_publications(
        self,
        keywords: list[str],
        min_pubyear: int = SCOPUS_SEARCH_MIN_PUBYEAR,
        max_pages: int = SCOPUS_SEARCH_MAX_PAGES,
    ) -> Iterator[list[ParsedAuthor]]:
        query = GET_PUBLICATION_BY_MIN_PUBYEAR_AND_KEYWORDS.format(
            max_pages=max_pages, min_pubyear=min_pubyear, keywords=" OR ".join(keywords)
        )
        return self._get_authors_and_publications(query=query)

    def _get_authors_and_publications(self, query: str) -> list[ParsedAuthor]:
        params = {"query": query, "view": "COMPLETE"}
        try:
            response = self.scopus_handler.get_abstracts_and_citations(params=params)
        except HTTPError as e:
            self.logger.error(
                f"Could not get authors and publication by query={query}, details: {e}"
            )
            raise
        parsed_authors = []
        for page in response:
            for entry in page.get("search-results", {}).get("entry", []):
                if "author" not in entry:
                    continue

                publication = self._parse_publication(entry)
                if publication:
                    authors = self._parse_authors(entry, publication)
                    if authors:
                        parsed_authors.extend(authors)
            break
        return parsed_authors

    def _parse_publication(self, entry: dict) -> ParsedPublication | None:
        try:
            return ParsedPublication(
                doi=entry.get("prism:doi"),
                title=entry.get("dc:title"),
                year=int(entry.get("prism:coverDate").split("-")[0]),
                abstract=entry.get("dc:description", ""),
                citation_count=entry.get("citedby-count"),
            )
        except ValidationError as e:
            self.logger.error(
                f"Error while parsing Publication from: {entry}, details: {e}"
            )
            return None

    def _parse_authors(
        self, entry: dict, publication: ParsedPublication
    ) -> ParsedAuthor | None:
        try:
            authors = []
            for author in entry.get("author", []):
                authors.append(
                    ParsedAuthor(
                        author_external_id=author.get("authid"),
                        first_name=author.get("given-name"),
                        last_name=author.get("surname"),
                        source=Source.Scopus,
                        publication=publication,
                    )
                )
            return authors
        except ValidationError as e:
            self.logger.error(f"Error while parsing Author from: {entry}, details: {e}")
            return None

    def get_author_affiliation(self, author_id: str) -> str | None:
        params = {"view": "ENHANCED"}
        author_response = self.scopus_handler.get_author_by_id(
            author_id=author_id, params=params
        )
        return self._extract_affiliation(author_response)

    @staticmethod
    def _extract_affiliation(author_response: dict) -> str | None:
        profile = author_response.get("author-retrieval-response", [{}])[0].get(
            "author-profile", {}
        )
        affiliation = profile.get("affiliation-current", {}).get("affiliation", {})
        if isinstance(affiliation, list):
            return affiliation[0].get("ip-doc", {}).get("afdispname")
        return affiliation.get("ip-doc", {}).get("afdispname")
