from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    is_admin: Mapped[bool]
    sessions: Mapped[list["UserSession"]] = relationship(back_populates="user")
    searches: Mapped[list["Search"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User<{self.email}>"
