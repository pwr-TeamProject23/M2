from backend.src.data_sources.connectors.web_scraper import WebScraper
from backend.src.data_sources.handlers.abstract import AbstractHandler


class ScopusHandler(AbstractHandler):
    def __init__(self) -> None:
        self.url = "https://www.scopus.com"
        self.scraper = WebScraper(self.url)

    def get_authors(self):
        return ["Lech Madeyski"]
