from pydantic import BaseModel
from src.common.models import SearchTaskStatus
from src.api_parsers.models import Source


class HistoryEntity(BaseModel):
    id: int
    index: int
    status: SearchTaskStatus
    filename: str


HistoryResponseModel = list[HistoryEntity]


class PublicationResponseModel(BaseModel):
    doi: str | None
    title: str
    year: int
    venues: list[str] | None
    abstract: str | None
    citationCount: int | None
    similarityScore: float | None


class AuthorResponseModel(BaseModel):
    id: int
    firstName: str
    lastName: str
    email: str | None
    source: Source
    publication: PublicationResponseModel


class SuggestionsResponseModel(BaseModel):
    authors: list[AuthorResponseModel]
    venues: set[str] | None


class DetailsResponseModel(BaseModel):
    affiliation: str | None


class SearchTaskCreationResponseModel(BaseModel):
    filename: str


class StatusResponseModel(BaseModel):
    status: SearchTaskStatus


class FilenameResponseModel(BaseModel):
    file_name: str
