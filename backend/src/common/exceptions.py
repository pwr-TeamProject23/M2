from typing import Any
from fastapi import HTTPException


class NotFound(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(404, "Not found", headers)

    
class Unauthorized(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(403, "Unauthorized", headers)
