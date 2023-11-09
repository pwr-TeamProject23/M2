from collections.abc import Iterator
from logging import getLogger

from backend.src.api_handlers.core import BaseRestHandler
from backend.src.api_handlers.dblp.pagination import OffsetPagination
from backend.src.config import DBLP_PAGE_SIZE


class DblpHandler:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.root_url = "https://dblp.org"
        self.rest_handler = BaseRestHandler(self.root_url, logger=self.logger)
        self.offset_pagination = OffsetPagination(self.rest_handler, DBLP_PAGE_SIZE)

    def get_publications(self, query: str | None) -> Iterator:
        return self.offset_pagination.paginate(query=query, url_path="/search/publ/api")

    def get_authors(self, query: str | None) -> Iterator:
        return self.offset_pagination.paginate(
            query=query, url_path="/search/author/api", max_requests=1, time_units=10
        )

    def get_venues(self, query: str | None) -> Iterator:
        return self.offset_pagination.paginate(
            query=query, url_path="/search/venue/api"
        )
