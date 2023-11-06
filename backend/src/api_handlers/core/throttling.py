import time
from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from logging import getLogger

from requests import Response
from requests.exceptions import HTTPError

from backend.src.api_handlers.core.exceptions import QuotaExceededException
from backend.src.config import API_RETRY_AFTER_THRESHOLD


class Throttling:
    def __init__(
        self,
        max_requests: int,
        time_unit: int,
        retry_after_field: str = "Retry-After",
    ):
        self.logger = getLogger(__name__)
        self.max_requests = max_requests
        self.time_unit = time_unit
        self.retry_after_field = retry_after_field
        self._remaining_requests = max_requests
        self._last_request_time = None

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            while True:
                self.check_request_limit()
                try:
                    response = func(*args, **kwargs)
                    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                        self.retry_after(response)
                        continue
                    self._remaining_requests -= 1
                    self._last_request_time = time.time()
                    return response
                except HTTPError as err:
                    if err.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                        self.retry_after(err.response)
                    else:
                        raise

        return wrapper

    def check_request_limit(self) -> None:
        if self._remaining_requests <= 0:
            current_time = time.time()
            elapsed_time = current_time - self._last_request_time
            if elapsed_time < self.time_unit:
                retry_after = int(self.time_unit - elapsed_time)
                self.logger.debug(
                    f"Waiting for {retry_after} seconds before retrying..."
                )
                time.sleep(retry_after)
            self._remaining_requests = self.max_requests

    def retry_after(self, response: Response) -> None:
        retry_after = int(response.headers.get(self.retry_after_field, 1))
        if retry_after > API_RETRY_AFTER_THRESHOLD:
            raise QuotaExceededException(retry_after)
        self.logger.warning(f"Received HTTP 429. Waiting for {retry_after} seconds...")
        time.sleep(retry_after)
        self._remaining_requests = self.max_requests
