from typing import Optional
from pydantic import BaseModel

from src.models.upload import CeleryTaskStatus


class HistoryEntity(BaseModel):
    id: int
    index: int
    status: CeleryTaskStatus
    filename: str


HistoryResponseModel = list[HistoryEntity]


class AuthorResponseModel(BaseModel):
    id: int
    name: str
    src: str
    year: int
    title: str
    affiliation: str
    venue: Optional[str]


class SuggestionsResponseModel(BaseModel):
    authors: list[AuthorResponseModel]
    venues: list[Optional[str]]


class DetailsResponseModel(BaseModel):
    affiliation: str
