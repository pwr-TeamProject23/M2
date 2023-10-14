from logging import getLogger

from backend.src.services.dblp.author import DblpAuthorHandler


class Dblp:
    def __init__(self):
        self.logger = getLogger(__name__)
        self.author_handler = DblpAuthorHandler()
    
    def get_authors(self, query: str) -> dict:
        return self.author_handler.get_authors(query=query)
