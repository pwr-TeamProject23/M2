from collections.abc import Iterator
from http import HTTPMethod
from logging import getLogger
from requests import Response

from src.api_handlers.core import BaseRestHandler
from src.api_handlers.scopus.pagination import OffsetPagination
from src.api_handlers.core.throttling import Throttling
from src.config import SCOPUS_API_KEY, SCOPUS_LONG_PAGE_SIZE, SCOPUS_SHORT_PAGE_SIZE


class ScopusHandler:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.root_url = "https://api.elsevier.com"
        self.rest_handler = BaseRestHandler(self.root_url, logger=self.logger)
        self.offset_pagination = OffsetPagination(self.rest_handler)
        self.max_author_requests = 3
        self.author_time_units = 1

    def get_affiliations(self, params: dict) -> Iterator:
        return self.offset_pagination.paginate(
            params=params,
            url_path="/content/search/affiliation",
            page_size=SCOPUS_LONG_PAGE_SIZE,
            headers={"X-ELS-APIKey": SCOPUS_API_KEY},
        )

    def get_authors(
        self,
        params: dict,
    ) -> Iterator:
        return self.offset_pagination.paginate(
            params=params,
            url_path="/content/search/author",
            page_size=SCOPUS_LONG_PAGE_SIZE,
            max_requests=2,
            time_units=1,
            headers={"X-ELS-APIKey": SCOPUS_API_KEY},
        )

    def get_abstracts_and_citations(self, params: dict) -> Iterator:
        return self.offset_pagination.paginate(
            params=params,
            url_path="/content/search/scopus",
            headers={"X-ELS-APIKey": SCOPUS_API_KEY},
            page_size=SCOPUS_SHORT_PAGE_SIZE,
        )

    @Throttling("max_author_requests", "author_time_units", "X-RateLimit-Reset")
    def _get_author_by_id(self, author_id: str, params: dict) -> Response:

        return self.rest_handler.request(
            method=HTTPMethod.GET,
            url_path=f"/content/author/author_id/{author_id}",
            params={**params},
            headers={"X-ELS-APIKey": SCOPUS_API_KEY, "Accept": "application/json"},
        )

    def get_author_by_id(self, author_id: str, params: dict) -> dict:
        return self._get_author_by_id(author_id, params).json()
