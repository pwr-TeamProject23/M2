from backend.src.api_utility.dblp import BaseDblpHandler


class DblpAuthorHandler(BaseDblpHandler):
    def __init__(self):
        super().__init__("author")

    def get_authors(self, query: str, response_format: str = "json") -> dict:
        return self.request("get", params={"q": query, "format": response_format})
