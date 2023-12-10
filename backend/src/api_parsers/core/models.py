from enum import Enum

from pydantic import BaseModel, ConfigDict


class Source(str, Enum):
    DBLP = "DBLP"
    GoogleScholar = "Google Scholar"
    Scopus = "Scopus"


class ParsedPublication(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    doi: str | None = None
    title: str
    year: int
    venues: list[str] | None = None
    abstract: str | None = None
    citation_count: int | None = 0
    similarity_score: float | None = 0.0


class ParsedAuthor(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    author_external_id: str
    first_name: str
    last_name: str
    affiliation: str | None = None
    email: str | None = None
    source: Source
    publication: ParsedPublication
