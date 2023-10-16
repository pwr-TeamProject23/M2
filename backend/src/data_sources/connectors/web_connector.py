import requests


class WebConnector:
    def __init__(self, url) -> None:
        self.url = url

    def _request(self, method: str, **params) -> requests.Response:
        return requests.request(method=method, url=self.url, params=params)

    def get_document(self) -> str:
        return self._request("get").content

    def get(self) -> dict:
        return self._request("get").json()
