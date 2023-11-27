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
    venue: str | None
    abstract: str
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

    def get_attrs(self) -> dict:
        return {
            "name": f"{self.first_name} {self.last_name}",
            "affiliation": self.affiliation,
            "title": self.publication.title,
            "year": self.publication.year,
            "source": self.source,
            "venue": self.publication.venue,
        }
