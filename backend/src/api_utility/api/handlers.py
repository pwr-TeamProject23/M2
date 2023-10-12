from backend.src.api_utility.api.core import BaseRestService
from backend.src.api_utility.auth import BaseTokenAuth


class BaseHandler:
    """Base class representing REST API service handler."""

    def __init__(
        self,
        auth: BaseTokenAuth,
        service: BaseRestService,
        root_url: str | None = None,
    ):
        self.auth = auth
        self.service = service
        self._root_url = root_url

    @property
    def root_url(self) -> str | None:
        return self._root_url or getattr(self.auth, "root_url", None)

    def request(self, action: str, **kwargs) -> dict:
        return self.service.request_endpoint(
            action, auth=self.auth, root_url=self.root_url, **kwargs
        )
