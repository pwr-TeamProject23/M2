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
        max_requests_attr: str,
        time_units_attr: str,
        retry_after_field: str = "Retry-After",
    ):
        self.logger = getLogger(__name__)
        self.max_requests_attr = max_requests_attr
        self.time_units_attr = time_units_attr
        self.retry_after_field = retry_after_field
        self._remaining_requests = None
        self._last_request_time = None
        self.max_requests = None
        self.time_units = None

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(obj, *args, **kwargs):
            if self.max_requests is None and self.time_units is None:
                self.max_requests = getattr(obj, self.max_requests_attr)
                self.time_units = getattr(obj, self.time_units_attr)
                self._remaining_requests = self.max_requests

            while True:
                self._check_request_limit()
                try:
                    response = func(obj, *args, **kwargs)
                    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                        self._retry_after(response)
                        continue
                    self._remaining_requests -= 1
                    self._last_request_time = time.time()
                    return response
                except HTTPError as err:
                    if err.response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                        self._retry_after(err.response)
                    else:
                        raise

        return wrapper

    def _check_request_limit(self) -> None:
        if self._remaining_requests <= 0:
            current_time = time.time()
            elapsed_time = current_time - self._last_request_time
            if elapsed_time < self.time_units:
                retry_after = int(self.time_units - elapsed_time)
                self.logger.debug(
                    f"Waiting for {retry_after} seconds before retrying..."
                )
                time.sleep(retry_after)
            self._remaining_requests = self.max_requests

    def _retry_after(self, response: Response) -> None:
        retry_after = int(response.headers.get(self.retry_after_field, 1))
        if retry_after > API_RETRY_AFTER_THRESHOLD:
            raise QuotaExceededException(retry_after)
        self.logger.warning(f"Received HTTP 429. Waiting for {retry_after} seconds...")
        time.sleep(retry_after)
        self._remaining_requests = self.max_requests
