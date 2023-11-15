from sqlalchemy.orm import mapped_column, Mapped

from src.models import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    password: Mapped[str]
    is_admin: Mapped[bool]

    def __repr__(self) -> str:
        return f"User<{self.email}>"
