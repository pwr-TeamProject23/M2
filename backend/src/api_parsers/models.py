from pydantic import BaseModel
from enum import Enum


class Source(str, Enum):
    SCOPUS = "SCOPUS"
    DBLP = "DBLP"
    SCHOLAR = "SCHOLAR"


class Publication(BaseModel):
    title: str
    abstract: str
    citations: int
    year: int
    source_api: Source


class Author(BaseModel):
    first_name: str
    last_name: str
    api_id: str
    affiliation: str
    publication: Publication
