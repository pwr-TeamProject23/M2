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

    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("upload.id"))
    author_external_id: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    affiliation: Mapped[str]
    email: Mapped[str | None]
    source: Mapped[Source]
    upload: Mapped["Upload"] = relationship(back_populates="authors")

    def __repr__(self) -> str:
        return f"Author<{self.first_name} {self.last_name}>"
