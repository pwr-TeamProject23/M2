from pydantic import BaseModel
from enum import Enum


class Source(str, Enum):
    DBLP = "DBLP"
    GoogleScholar = "Google Scholar"
    Scopus = "Scopus"


class Publication(BaseModel):
    doi: str | None
    title: str
    year: int
    venues: list[str] | None
    abstract: str | None
    citation_count: int | None
    similarity_score: float | None


class Author(BaseModel):
    author_external_id: str
    first_name: str
    last_name: str
    affiliation: str | None
    email: str | None
    source: Source
    publication: Publication
