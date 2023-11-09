class QuotaExceededException(Exception):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(f"Quota exceeded. Try again in {retry_after} seconds.")
