from pydantic import BaseModel, ConfigDict, Field
from src.api_parsers.models import Source
from src.common.models import SearchTaskStatus


class HistoryEntity(BaseModel):
    id: int
    index: int
    status: SearchTaskStatus
    filename: str


HistoryResponseModel = list[HistoryEntity]


class PublicationResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doi: str | None
    title: str
    year: int
    venues: list[str] | None
    abstract: str | None
    citation_count: int | None = Field(..., serialization_alias="citationCount")
    similarity_score: float | None = Field(..., serialization_alias="similarityScore")


class AuthorResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_external_id: str = Field(..., serialization_alias="authorExternalId")
    first_name: str = Field(..., serialization_alias="firstName")
    last_name: str = Field(..., serialization_alias="lastName")
    email: str | None
    source: Source
    publication: PublicationResponseModel


class SuggestionsResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
