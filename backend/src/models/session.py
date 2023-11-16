from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.models import BaseModel


class UserSession(BaseModel):
    __tablename__ = "user_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    session_id: Mapped[str]
    expiration_datetime: Mapped[datetime]
