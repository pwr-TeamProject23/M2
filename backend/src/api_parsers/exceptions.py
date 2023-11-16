class NoAuthorsException(Exception):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"There are no results for keywords: {query}.")


class RetrievalFailedException(Exception):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"Failed to retrieve results for keywords: {query}")
