from itertools import islice
from logging import getLogger

from pydantic import ValidationError
from requests import HTTPError
from src.api_handlers.dblp import DblpHandler
from src.api_parsers.core.models import ParsedAuthor, ParsedPublication, Source
from src.config import DBLP_SEARCH_MAX_PAGES


class DblpParser:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.dblp_handler = DblpHandler()

    def get_authors_and_publications(
        self, keywords: list[str], max_pages: int = DBLP_SEARCH_MAX_PAGES
    ) -> list[ParsedAuthor]:
        try:
            response = self.dblp_handler.get_publications(keywords[0])
            parsed_authors = []

            for page in islice(response, max_pages):
                for entry in page.get("result", {}).get("hits", {}).get("hit", []):
                    publication = self._parse_publication(entry)
                    if publication:
                        authors = self._parse_authors(entry, publication)
                        if authors:
                            parsed_authors.extend(authors)
            return parsed_authors
        except HTTPError as e:
            self.logger.error(
                f"Could not get authors and publications from DBLP by keywords: {keywords}, details: {e}"
            )
            raise

    def _parse_publication(self, entry: dict) -> ParsedPublication | None:
        try:
            entry = entry["info"]
            venues = entry.get("venue")
            return ParsedPublication(
                doi=entry.get("doi"),
                title=entry.get("title"),
                year=entry.get("year"),
                venues=[venues] if isinstance(venues, str) else venues,
            )
        except ValidationError as e:
            self.logger.error(
                f"Error while parsing Publication from: {entry}, details: {e}"
            )
            return None

    def _parse_authors(
        self, entry: dict, publication: ParsedPublication
    ) -> list[ParsedAuthor] | None:
        try:
            entry = entry["info"]
            authors = entry.get("authors", {}).get("author", [])
            if isinstance(authors, dict):
                authors = [authors]
            parsed_authors = []
            for author in authors:
                parsed_author = ParsedAuthor(
                    author_external_id=author.get("@pid"),
                    first_name=author.get("text", "").split(" ")[0],
                    last_name=author.get("text", "").split(" ")[-1],
                    affiliation=author.get("affiliation"),
                    email=author.get("email"),
                    source=Source.DBLP,
                    publication=publication,
                )
                parsed_authors.append(parsed_author)
            return parsed_authors
        except ValidationError as e:
            self.logger.error(
                f"Error while parsing Authors from: {entry}, details: {e}"
            )
            return None

    def get_author_affiliation(self, author_name: str, author_id: str) -> str | None:
        author_response = self.dblp_handler.get_authors(author_name)
        for page in author_response:
            affiliation = self._extract_affiliation(author_id, page)
            if affiliation:
                return affiliation

    @staticmethod
    def _extract_affiliation(author_id: str, page: dict) -> str | None:
        for entry in page.get("result", {}).get("hits", {}).get("hit", []):
            info = entry.get("info", {})
            if not info.get("url", "").endswith(author_id):
                continue
            notes = info.get("notes", {}).get("note", {})
            if isinstance(notes, list):
                return next(
                    (
                        note.get("text")
                        for note in notes
                        if note.get("@type") == "affiliation"
                    ),
                    None,
                )
            if notes.get("@type") == "affiliation":
                return notes.get("text")
            return None
