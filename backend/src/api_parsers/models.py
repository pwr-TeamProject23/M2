from pydantic import BaseModel
from enum import Enum


class Source(str, Enum):
    SCOPUS = 'SCOPUS'
    DBLP = 'DBLP'
    SCHOLAR = 'SCHOLAR'


class Publication(BaseModel):
    title: str
    abstract: str
    citations: int
    source_api: Source


class Author(BaseModel):
    name: str
    api_id: str
    publication: Publication
