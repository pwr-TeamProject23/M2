from collections.abc import Callable, Iterator
from functools import wraps
from logging import getLogger


class OffsetPagination:
    def __init__(self, page_size: int):
        self.logger = getLogger(__name__)
        self.page_size = page_size

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Iterator:
            offset, page_count = 0, 0

            while True:
                pagination_params = self.get_pagination_params(offset)
                response = func(
                    *args, **kwargs, pagination_params=pagination_params
                ).json()
                yield response

                offset += self.page_size
                page_count += 1
                if self.last_page_reached(response, offset):
                    self.logger.debug(f"Last page was reached, page_count={page_count}")
                    break

        return wrapper

    def get_pagination_params(self, offset: int) -> dict:
        return {"h": self.page_size, "f": offset}

    @staticmethod
    def last_page_reached(response: dict, offset: int) -> bool:
        return offset >= int(response["result"]["completions"]["@total"])
