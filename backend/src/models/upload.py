from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import BaseModel


class Upload(BaseModel):
    __tablename__ = "upload"

    id: Mapped[int] = mapped_column(primary_key=True)
    file_name: Mapped[int]
    user_id: Mapped[int]
    error: Mapped[bool]
    reviewers: Mapped["Reviewer"] = relationship(back_populates="upload")

    def __repr__(self) -> str:
        return f"Upload<{self.file_name}>"
