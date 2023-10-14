from backend.src.api_utility.api import BaseHandler
from backend.src.api_utility.auth import BaseTokenAuth
from backend.src.api_utility.sample_api import SAMPLE_API


class BaseSampleHandler(BaseHandler):
    def __init__(self, auth: BaseTokenAuth, service: str, root_url: str | None = None):
        super().__init__(SAMPLE_API[service], root_url)


class SampleHandler(BaseSampleHandler):
    def __init__(self, auth: BaseTokenAuth, root_url: str | None = None):
        super().__init__(auth, "sample_endpoint", root_url)

    def get_sample_data(self, params: dict = None) -> dict:
        return self.request("get", params=params or {})
