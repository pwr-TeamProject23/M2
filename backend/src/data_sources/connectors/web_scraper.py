from bs4 import BeautifulSoup
from web_connector import WebConnector


class WebScraper:
    def __init__(self, url) -> None:
        self.url = url

    def get_beautiful_soup(self) -> BeautifulSoup:
        page = WebConnector(self.url).get_document()
        return BeautifulSoup(page, "html.parser")
