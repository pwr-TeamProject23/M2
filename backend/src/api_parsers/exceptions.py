class NoAuthorsException(Exception):
    def __init__(self, query: str):
        self.query = query
        super().__init__(f"There are no results for keywords: {query}.")

        
class NoAffiliationException(Exception):
    def __init__(self, author_id: str):
        self.author_id = author_id
        super().__init__(f"No affiliation found for {author_id}.")


class DBLPQuotaExceededException(Exception):
    def __init__(self):
        super().__init__(f"Quota exceeded.")

