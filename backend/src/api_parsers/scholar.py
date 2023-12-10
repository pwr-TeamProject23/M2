from itertools import islice
from logging import getLogger

from pydantic import ValidationError
from scholarly import MaxTriesExceededException, scholarly
from src.api_parsers import ParsedAuthor, ParsedPublication, Source
from src.config import (
    SCHOLAR_SEARCH_MAX_AUTHORS_PER_PUBLICATION,
    SCHOLAR_SEARCH_MAX_PUBLICATIONS,
    SCHOLAR_SEARCH_YEAR_LOW,
)


class ScholarParser:
    def __init__(self):
        self.logger = getLogger(__name__)

    def get_authors_and_publications(
        self,
        keywords: list[str],
        year_low: int = SCHOLAR_SEARCH_YEAR_LOW,
        max_publications: int = SCHOLAR_SEARCH_MAX_PUBLICATIONS,
    ) -> list[str]:
        try:
            response = scholarly.search_pubs(
                query=" ".join(keywords), year_low=year_low
            )
            parsed_authors = []
            for entry in islice(response, max_publications):
                publication = self._parse_publication(entry)
                if publication:
                    authors = self._parse_authors(entry, publication)
                    if authors:
                        parsed_authors.extend(authors)
            return parsed_authors
        except MaxTriesExceededException as e:
            self.logger.error(f"Exceeded number of allowed API calls, details: {e}")
            raise

    def _parse_publication(self, entry: dict) -> ParsedPublication | None:
        try:
            bib = entry["bib"]
            return ParsedPublication(
                title=bib.get("title"),
                year=bib.get("pub_year"),
                venues=[bib.get("venue")],
                abstract=bib.get("abstract"),
                citation_count=entry.get("num_citations"),
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
            author_ids = entry["author_id"][:SCHOLAR_SEARCH_MAX_AUTHORS_PER_PUBLICATION]
            parsed_authors = []
            for author_id in author_ids:
                if not author_id:
                    continue
                author = scholarly.search_author_id(author_id)
                split_name = author.get("name", "").split()
                first_name, last_name = split_name[0], " ".join(split_name[1:])

                parsed_authors.append(
                    ParsedAuthor(
                        author_external_id=author.get("scholar_id"),
                        first_name=first_name,
                        last_name=last_name,
                        affiliation=author.get("affiliation"),
                        source=Source.GoogleScholar,
                        publication=publication,
                    )
                )
            return parsed_authors
        except ValidationError as e:
            self.logger.error(
                f"Error while parsing Authors from: {entry}, details: {e}"
            )
            return None
