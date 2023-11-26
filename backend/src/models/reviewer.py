from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import BaseModel
import enum


class Source(enum.Enum):
    DBLP = "DBLP"
    GoogleScholar = "Google Scholar"
    Scopus = "Scopus"


class Reviewer(BaseModel):
    __tablename__ = "reviewer"

    id: Mapped[int] = mapped_column(primary_key=True)
    upload_id: Mapped[int] = mapped_column(ForeignKey("upload.id"))
    name: Mapped[str]
    surname: Mapped[str]
    faculty: Mapped[str]
    email: Mapped[str]
    source: Mapped[Source]
    article_doi: Mapped[str]
    upload: Mapped["Upload"] = relationship(back_populates="reviewers")

    def __repr__(self) -> str:
        return f"Upload<{self.name}>"
