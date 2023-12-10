from collections.abc import Iterator
from enum import Enum
from http import HTTPMethod
from logging import getLogger

from requests import Response
from src.api_handlers.core import BaseRestHandler
from src.api_handlers.core.throttling import Throttling


class DblpResponseFormat(str, Enum):
    JSON = "json"


class OffsetPagination:
    max_requests: int
    time_units: int

    def __init__(self, rest_handler: BaseRestHandler, page_size: int):
        self.logger = getLogger(__name__)
        self.rest_handler = rest_handler
        self.page_size = page_size

    def paginate(
        self,
        *,
        query: str,
        url_path: str,
        method: HTTPMethod | str = HTTPMethod.GET,
        max_requests: int = 1,
        time_units: int = 1,
    ) -> Iterator:
        self.max_requests = max_requests
        self.time_units = time_units
        offset, page_count = 0, 0

        while True:
            response = self._get_page(method, query, url_path, offset).json()
            yield response

            offset += self.page_size
            page_count += 1
            if self._last_page_reached(response, offset):
                self.logger.debug(f"Last page was reached, page_count={page_count}")
                break

    @Throttling("max_requests", "time_units")
    def _get_page(
        self, method: HTTPMethod | str, query: str, url_path: str, offset: int
    ) -> Response:
        pagination_params = {"h": self.page_size, "f": offset}
        return self.rest_handler.request(
            method,
            url_path,
            params={
                "q": query,
                "format": DblpResponseFormat.JSON,
                **pagination_params,
            },
        )

    @staticmethod
    def _last_page_reached(response: dict, offset: int) -> bool:
        return offset >= int(response["result"]["completions"]["@total"])
