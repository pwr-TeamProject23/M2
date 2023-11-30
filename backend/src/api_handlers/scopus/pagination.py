from collections.abc import Iterator
from http import HTTPMethod
from logging import getLogger
from urllib.parse import parse_qs, urlparse

from requests import Response
from src.api_handlers.core import BaseRestHandler
from src.api_handlers.core.throttling import Throttling


class OffsetPagination:
    max_requests: int
    time_units: int

    def __init__(self, rest_handler: BaseRestHandler):
        self.logger = getLogger(__name__)
        self.rest_handler = rest_handler

    def paginate(
        self,
        *,
        params: dict,
        url_path: str,
        method: HTTPMethod | str = HTTPMethod.GET,
        page_size: int = 25,
        max_requests: int = 9,
        time_units: int = 1,
        **kwargs,
    ) -> Iterator:
        self.max_requests = max_requests
        self.time_units = time_units
        start, page_count = 0, 0
        response, next_page_url = None, None

        while True:
            if page_count > 0:
                start = parse_qs(urlparse(next_page_url).query).get("start")[0]
            response = self._get_page(
                params, method, url_path, start, page_size, **kwargs
            ).json()
            yield response

            page_count += 1
            next_page_url = self._get_next_page_url(response)
            if next_page_url is None:
                self.logger.debug(f"Last page was reached, page_count={page_count}")
                break

    @Throttling("max_requests", "time_units", "X-RateLimit-Reset")
    def _get_page(
        self,
        params: dict,
        method: HTTPMethod | str,
        url_path: str,
        start: int,
        count: int,
        **kwargs,
    ) -> Response:
        pagination_params = {"start": start, "count": count}
        return self.rest_handler.request(
            method, url_path, params={**params, **pagination_params}, **kwargs
        )

    @staticmethod
    def _get_next_page_url(response: dict) -> str | None:
        return next(
            filter(
                lambda link: link.get("@ref") == "next",
                response["search-results"]["link"],
            ),
            {},
        ).get("@href")
