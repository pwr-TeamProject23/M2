from http import HTTPStatus

from fastapi import HTTPException


class NotFoundException(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(HTTPStatus.NOT_FOUND, "Not found", headers)


class ForbiddenException(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(HTTPStatus.FORBIDDEN, "Forbidden", headers)


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        headers: dict[str, str] | None = None,
    ):
        super().__init__(HTTPStatus.UNAUTHORIZED, "Unauthorized", headers)
