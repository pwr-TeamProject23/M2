from backend.src.authors.connectors.web_connector import WebConnector
from backend.src.authors.handlers.abstract_handler import AuthorsHandler


class DBLPHandler(AuthorsHandler):
    def __init__(self) -> None:
        self.url = "https://dblp.org/"
        self.connector = WebConnector(self.url)

    def get_authors(self):
        return ["Lech Madeyski"]
