from backend.src.data_sources.connectors import WebConnector
from backend.src.data_sources.handlers.abstract import AbstractHandler


class DBLPHandler(AbstractHandler):
    def __init__(self) -> None:
        self.url = "https://dblp.org"
        self.connector = WebConnector(self.url)

    def get_authors(self):
        return ["Lech Madeyski"]
