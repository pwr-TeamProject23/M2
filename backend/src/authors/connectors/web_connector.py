import requests


class WebConnector:
    def __init__(self, url) -> None:
        self.url = url

    def _request(self, **params) -> requests.Response:
        return requests.get(self.url, params=params)

    def get_document(self) -> str:
        return self._request().content

    def get(self) -> dict:
        return self._request().json()
