from abc import ABC, abstractmethod

from backend.src.api_utility.auth.token import BaseToken


class BaseTokenAuth(ABC):
    """
    Abstract class that is a blueprint for requesting,
    storing and accessing authentication tokens.
    """

    def __init__(self, root_url: str, auth_data: dict):
        self.root_url = root_url
        self._auth_data = auth_data
        self._token = None

    @abstractmethod
    def _request_new_token(self, refresh: bool = False) -> BaseToken:
        pass

    @property
    @abstractmethod
    def access_token(self) -> str:
        pass
