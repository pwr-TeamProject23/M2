class EndpointNotFoundError(Exception):
    def __init__(self, action: str):
        super().__init__(f"Endpoint for action {action} not found")


class RequestResponseError(Exception):
    def __init__(self, status_code: int, response: str):
        super().__init__(f"Server responded with status code: {status_code}", response)
