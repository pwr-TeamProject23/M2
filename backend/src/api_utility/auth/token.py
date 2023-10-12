from datetime import datetime, timedelta
from enum import Enum


class TokenType(str, Enum):
    Bearer = "Bearer"


class BaseToken:
    """Base class representing authentication token."""

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        expires_in: int | None = None,
        refresh_expires_in: int | None = None,
        token_type: TokenType | str = TokenType.Bearer,
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.refresh_expires_in = refresh_expires_in
        self.expiration_date = self._get_expiration_datetime(expires_in)
        self.refresh_expiration_date = self._get_expiration_datetime(refresh_expires_in)
        self.token_type = token_type

    def __bool__(self):
        return self.is_valid_refresh

    @property
    def is_valid(self) -> bool:
        return self._is_expired(self.expiration_date)

    @property
    def is_valid_refresh(self) -> bool:
        return self._is_expired(self.refresh_expiration_date)

    @staticmethod
    def _is_expired(expiration_date: datetime | None) -> bool:
        return datetime.now() < expiration_date if expiration_date else True

    @staticmethod
    def _get_expiration_datetime(seconds: int | None) -> datetime:
        return datetime.now() + timedelta(seconds=seconds) if seconds else None
