from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel


class Publication(BaseModel):
    __tablename__ = "publication"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    doi: Mapped[str | None]
    title: Mapped[str]
    year: Mapped[int]
    venue: Mapped[str | None]
    abstract: Mapped[str | None]
    citation_count: Mapped[int | None]
    similarity_score: Mapped[float | None]
    author: Mapped["Author"] = relationship(back_populates="publications")

    def __repr__(self) -> str:
        return f"Publication<{self.title}>"
