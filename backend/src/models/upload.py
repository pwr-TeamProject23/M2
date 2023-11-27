from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel


class CeleryTaskStatus(str, Enum):
    #: Task state is unknown (assumed pending since you know the id).
    PENDING = "PENDING"
    #: Task was received by a worker (only used in events).
    RECEIVED = "RECEIVED"
    #: Task was started by a worker (:setting:`task_track_started`).
    STARTED = "STARTED"
    #: Task succeeded
    SUCCESS = "SUCCESS"
    #: Task failed
    FAILURE = "FAILURE"
    #: Task was revoked.
    REVOKED = "REVOKED"
    #: Task was rejected (only used in events).
    REJECTED = "REJECTED"
    #: Task is waiting for retry.
    RETRY = "RETRY"
    IGNORED = "IGNORED"


class Upload(BaseModel):
    __tablename__ = "upload"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    file_name: Mapped[str]
    task_id: Mapped[str | None]
    status: Mapped[CeleryTaskStatus]
    user: Mapped["User"] = relationship(back_populates="uploads")
    authors: Mapped[list["Author"]] = relationship(back_populates="upload")

    def __repr__(self) -> str:
        return f"Upload<{self.file_name}>"
