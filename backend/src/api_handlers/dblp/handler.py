from collections.abc import Iterator
from enum import Enum
from http import HTTPMethod
from logging import getLogger

from backend.src.api_handlers.core import BaseRestHandler, Throttling
from backend.src.api_handlers.dblp.pagination import OffsetPagination


class DblpResponseFormat(str, Enum):
    JSON = "json"


class DblpHandler:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.root_url = "https://dblp.org"
        self.rest_handler = BaseRestHandler(self.root_url, logger=self.logger)

    @OffsetPagination(page_size=1000)
    @Throttling(max_requests=1, time_unit=1)
    def get_publications(
        self,
        query: str | None,
        pagination_params: dict | None = None,
    ) -> Iterator:
        return self.rest_handler.request(
            HTTPMethod.GET,
            "/search/publ/api",
            params={
                "q": query,
                "format": DblpResponseFormat.JSON,
                **(pagination_params or {}),
            },
        )

    @OffsetPagination(page_size=1000)
    @Throttling(max_requests=1, time_unit=1)
    def get_authors(
        self,
        query: str | None,
        pagination_params: dict | None = None,
    ) -> Iterator:
        return self.rest_handler.request(
            HTTPMethod.GET,
            "/search/author/api",
            params={
                "q": query,
                "format": DblpResponseFormat.JSON,
                **(pagination_params or {}),
            },
        )

    @OffsetPagination(page_size=1000)
    @Throttling(max_requests=1, time_unit=1)
    def get_venues(
        self,
        query: str | None,
        pagination_params: dict | None = None,
    ) -> Iterator:
        return self.rest_handler.request(
            HTTPMethod.GET,
            "/search/venue/api",
            params={
                "q": query,
                "format": DblpResponseFormat.JSON,
                **(pagination_params or {}),
            },
        )
