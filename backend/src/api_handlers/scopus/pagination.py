from collections.abc import Callable, Iterator
from functools import wraps
from logging import getLogger
from urllib.parse import urlparse


class OffsetPagination:
    def __init__(self, page_size):
        self.logger = getLogger(__name__)
        self.page_size = page_size

    def __call__(self, func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs) -> Iterator:
            page_count = 0
            response, next_page_url = None, None

            while True:
                if page_count > 0:
                    kwargs.pop("query", None)
                    next_page_query = urlparse(next_page_url).query
                    response = func(
                        *args, **kwargs, next_page_query=next_page_query
                    ).json()
                else:
                    response = func(*args, **kwargs, count=self.page_size).json()
                yield response

                page_count += 1
                next_page_url = self.get_next_page_url(response)
                if next_page_url is None:
                    self.logger.debug(f"Last page was reached, page_count={page_count}")
                    break

        return wrapper

    @staticmethod
    def get_next_page_url(response: dict) -> str | None:
        return next(
            filter(
                lambda link: link.get("@ref") == "next",
                response["search-results"]["link"],
            ),
            {},
        ).get("@href")
