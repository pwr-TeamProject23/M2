from backend.src.data_sources.connectors.web_connector import WebConnector
from backend.src.data_sources.handlers.abstract import AbstractHandler


class GoogleScholarHandler(AbstractHandler):
    def __init__(self) -> None:
        self.url = "https://scholar.google.com"
        self.connector = WebConnector(self.url)

    def get_authors(self):
        return ["Lech Madeyski"]
