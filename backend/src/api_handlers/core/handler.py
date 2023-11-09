from http import HTTPMethod
from logging import Logger, getLogger

from requests import HTTPError, JSONDecodeError, Response, request


class BaseRestHandler:
    def __init__(self, root_url: str, logger: Logger | None = None):
        self.logger = logger or getLogger(__name__)
        self.root_url = root_url

    def request(
        self, method: HTTPMethod | str, url_path: str | None, **request_args
    ) -> Response:
        url = f"{self.root_url}{url_path}"
        try:
            self.logger.debug(
                f"Sending {method} request to URL={url} with args={request_args}"
            )
            response = request(str(method), url, **request_args)
            response.raise_for_status()
            return response
        except (HTTPError, JSONDecodeError) as err:
            self.logger.error(
                (
                    f"Error occurred while making request to URL={url}, method={method}, "
                    f"request_args={request_args}, details: {err}"
                ),
                exc_info=True,
            )
            raise
