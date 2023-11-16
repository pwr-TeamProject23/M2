class NoAuthorsException(Exception):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"There are no results for keywords: {query}.")
