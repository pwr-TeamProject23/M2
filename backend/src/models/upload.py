from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from src.models import BaseModel


class Upload(BaseModel):
    __tablename__ = "upload"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    file_name: Mapped[int]
    error: Mapped[bool]
    reviewers: Mapped["Reviewer"] = relationship(back_populates="upload")
    user: Mapped["User"] = relationship(back_populates="uploads")

    def __repr__(self) -> str:
        return f"Upload<{self.file_name}>"
