from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel


class Source(str, Enum):
    DBLP = "DBLP"
    GoogleScholar = "Google Scholar"
    Scopus = "Scopus"


class Author(BaseModel):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    search_id: Mapped[int | None] = mapped_column(
        ForeignKey("search.id", ondelete="CASCADE")
    )
    author_external_id: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    affiliation: Mapped[str | None]
    email: Mapped[str | None]
    source: Mapped[Source]
    search: Mapped["Search"] = relationship(back_populates="authors")
    publication: Mapped["Publication"] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Author<{self.first_name} {self.last_name}>"
