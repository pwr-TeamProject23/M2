from datetime import datetime

import bcrypt
from sqlalchemy.orm import Session
from src.common.postgres import SessionLocal
from src.common.repository import BaseRepository
from src.models.session import UserSession
from src.models.user import User


class UserRepository(BaseRepository[User]):
    __model__ = User

    @classmethod
    def create_user(
        cls,
        db_session: Session,
        email: str,
        password: str,
        is_admin: bool,
    ) -> User:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user = User(
            email=email,
            password=hashed_password,
            is_admin=is_admin,
        )

        return cls.create(db_session, user)

    @classmethod
    def create_super_user(cls, password: str, email: str) -> User:
        db_session = SessionLocal()
        return cls.create_user(
            db_session,
            password,
            email,
            is_admin=True,
        )


class UserSessionRepository(BaseRepository[UserSession]):
    __model__ = UserSession

    @classmethod
    def create_session(
        cls,
        db_session: Session,
        user_id: int,
        session_id: str,
        expiration_datetime: datetime,
    ) -> UserSession:
        user_session = UserSession(
            user_id=user_id,
            session_id=session_id,
            expiration_datetime=expiration_datetime,
        )
        return cls.create(db_session, user_session)
