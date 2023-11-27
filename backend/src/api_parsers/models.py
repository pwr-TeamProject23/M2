from pydantic import BaseModel
from enum import Enum


class Source(str, Enum):
    SCOPUS = "SCOPUS"
    DBLP = "DBLP"
    SCHOLAR = "SCHOLAR"


class Publication(BaseModel):
    title: str
    year: int
    venue: str | None
    citations: int | None
    abstract: str
    source_api: Source
    similarity_score: float | None


class Author(BaseModel):
    first_name: str
    last_name: str
    api_id: str
    affiliation: str | None
    publication: Publication

    def get_attrs(self) -> dict:
        return {
            'name': f'{self.first_name} {self.last_name}',
            'affiliation': self.affiliation,
            'title': self.publication.title,
            'year': self.publication.year,
            'source': self.publication.source_api,
            'venue': self.publication.venue
        }

