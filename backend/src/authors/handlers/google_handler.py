from authors.connectors.web_connector import WebConnector
from authors.handlers.abstract_handler import AuthorsHandler


class GoogleScholarHandler(AuthorsHandler):
    def __init__(self) -> None:
        self.url = "https://scholar.google.com/"
        self.connector = WebConnector(self.url)

    def get_authors(self):
        return ["Lech Madeyski"]
