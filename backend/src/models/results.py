from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from ..models import BaseModel


class Results(BaseModel):
    __tablename__ = "results"

    upload_id: Mapped[int] = mapped_column(ForeignKey("upload.id"), primary_key=True)
    reviewer_id: Mapped[int] = mapped_column(primary_key=True)
    upload: Mapped["Upload"] = relationship(back_populates="results")

    def __repr__(self) -> str:
        return f"Upload<{self.upload_id}>"
