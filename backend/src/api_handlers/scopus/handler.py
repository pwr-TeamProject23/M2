from collections.abc import Iterator
from http import HTTPMethod
from logging import getLogger

from backend.src.api_handlers.core import BaseRestHandler, Throttling
from backend.src.api_handlers.scopus.pagination import OffsetPagination
from backend.src.config import SCOPUS_API_KEY


class ScopusHandler:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.root_url = "https://api.elsevier.com"
        self.rest_handler = BaseRestHandler(self.root_url, logger=self.logger)

    @OffsetPagination(page_size=200)
    @Throttling(max_requests=9, time_unit=1, retry_after_field="X-RateLimit-Reset")
    def get_affiliations(self, **query_params) -> Iterator:
        return self.rest_handler.request(
            HTTPMethod.GET,
            "/content/search/affiliation",
            headers={"X-ELS-APIKey": SCOPUS_API_KEY},
            params={**query_params},
        )

    @OffsetPagination(page_size=200)
    @Throttling(max_requests=2, time_unit=1, retry_after_field="X-RateLimit-Reset")
    def get_authors(
        self,
        query: str | None = None,
        next_page_query: str | None = None,
        count: int | None = None,
    ) -> Iterator:
        return self.rest_handler.request(
            HTTPMethod.GET,
            f"/content/search/author?{next_page_query}",
            headers={"X-ELS-APIKey": SCOPUS_API_KEY},
            params={
                "count": count,
                "query": query,
            },
        )

    @OffsetPagination(page_size=200)
    @Throttling(max_requests=9, time_unit=1, retry_after_field="X-RateLimit-Reset")
    def get_abstracts_and_citations(self, **query_params) -> Iterator:
        return self.rest_handler.request(
            HTTPMethod.GET,
            "/content/search/scopus",
            headers={"X-ELS-APIKey": SCOPUS_API_KEY},
            params={"view": "COMPLETE", **query_params},
        )
