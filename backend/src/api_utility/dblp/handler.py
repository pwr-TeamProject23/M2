from backend.src.api_utility.api import BaseHandler
from backend.src.api_utility.dblp.api import DBLP_API


class BaseDblpHandler(BaseHandler):
    ROOT_URL = "https://dblp.org/search/publ/api"

    def __init__(self, service: str):
        super().__init__(DBLP_API[service], self.ROOT_URL)
