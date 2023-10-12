from collections.abc import Iterable
from dataclasses import dataclass

import requests

from backend.src.api_utility.api.exceptions import (
    EndpointNotFoundError,
    RequestResponseError,
)
from backend.src.api_utility.auth import BaseTokenAuth


@dataclass
class BaseRestEndpoint:
    action: str
    url_path: str
    method: str = "GET"


class BaseRestService:
    def __init__(self, service_name: str, endpoints: Iterable[BaseRestEndpoint]):
        self.service_name = service_name
        self._endpoints = self._register_endpoints(endpoints)
        self._url_pattern = "{root_url}{url_path}"

    def request_endpoint(
        self, action: str, root_url: str, auth: BaseTokenAuth | None = None, **kwargs
    ) -> dict:
        if action not in self._endpoints:
            raise EndpointNotFoundError(action)
        else:
            return self._request_endpoint(
                method=self._endpoints[action].method,
                url=self._get_url_for_request(
                    root_url, self._endpoints[action].url_path
                ),
                **self._get_args_for_request(auth, **kwargs),
            )

    @staticmethod
    def _request_endpoint(method: str, url: str, **kwargs) -> dict:
        # TODO: set up ssl verification (verify=True)
        response = requests.request(method, url, verify=False, **kwargs)
        if response.status_code >= 400:
            raise RequestResponseError(response.status_code, response.text)
        return response.json()

    @staticmethod
    def _register_endpoints(endpoints: Iterable[BaseRestEndpoint]) -> dict:
        return {endpoint.action: endpoint for endpoint in endpoints}

    def _get_url_for_request(self, root_url: str, url_path: str) -> str:
        return self._url_pattern.format(root_url=root_url, url_path=url_path)

    @staticmethod
    def _get_args_for_request(auth: BaseTokenAuth | None = None, **kwargs) -> dict:
        args = dict(headers={}, params={}, data={})
        args.update(kwargs)
        if auth:
            args["headers"]["Authorization"] = auth.access_token
        return args


class BaseRestApi:
    def __init__(self):
        self._services = {}

    def __setitem__(self, service_name: str, service: BaseRestService):
        self._services[service_name] = service

    def __getitem__(self, service_name):
        return self._services[service_name]
