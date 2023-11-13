
from sqlalchemy.orm import mapped_column, Mapped

from ..models import BaseModel
import enum


class Source(enum.Enum):
    DBLP = 1
    GoogleScholar = 2
    Scopus = 3


class Reviewer(BaseModel):
    __tablename__ = "reviewer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    faculty: Mapped[str]
    email: Mapped[str]
    source: Mapped[Source]
    article_doi: Mapped[str]

    def __repr__(self) -> str:
        return f"Upload<{self.name}>"
