from typing import Optional

from pydantic import BaseModel
from src.common.models import SearchTaskStatus


class HistoryEntity(BaseModel):
    id: int
    index: int
    status: SearchTaskStatus
    filename: str


HistoryResponseModel = list[HistoryEntity]


class AuthorResponseModel(BaseModel):
    id: int
    name: str
    src: str
    year: int | None
    title: str | None
    affiliation: str | None
    venue: Optional[str]


class SuggestionsResponseModel(BaseModel):
    authors: list[AuthorResponseModel]
    venues: list[Optional[str]]


class DetailsResponseModel(BaseModel):
    affiliation: str | None


class SearchTaskCreationResponseModel(BaseModel):
    filename: str


class StatusResponseModel(BaseModel):
    status: SearchTaskStatus
