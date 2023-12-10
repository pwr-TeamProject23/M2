from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.common.models import SearchTaskStatus
from src.models import BaseModel


class Search(BaseModel):
    __tablename__ = "search"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    file_name: Mapped[str]
    task_id: Mapped[str | None]
    status: Mapped[SearchTaskStatus]
    user: Mapped["User"] = relationship(back_populates="searches")
    authors: Mapped[list["Author"]] = relationship(
        back_populates="search", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Upload<{self.file_name}>"
