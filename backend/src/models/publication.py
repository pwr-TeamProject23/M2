from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel


class Publication(BaseModel):
    __tablename__ = "publication"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete="CASCADE"))
    doi: Mapped[str | None]
    title: Mapped[str]
    year: Mapped[int]
    venues: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)
    abstract: Mapped[str | None]
    citation_count: Mapped[int | None]
    similarity_score: Mapped[float | None]
    author: Mapped["Author"] = relationship(back_populates="publication")

    def __repr__(self) -> str:
        return f"Publication<{self.title}>"
