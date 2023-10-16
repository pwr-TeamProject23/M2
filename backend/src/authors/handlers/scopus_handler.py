from authors.connectors.web_scraper import WebScraper
from authors.handlers.abstract_handler import AuthorsHandler


class ScopusHandler(AuthorsHandler):
    def __init__(self) -> None:
        self.url = "https://www.scopus.com/"
        self.scraper = WebScraper(self.url)

    def get_authors(self):
        return ["Lech Madeyski"]
