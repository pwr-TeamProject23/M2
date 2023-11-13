from datetime import datetime
import bcrypt
from sqlalchemy.orm import Session

from src.models.user import User
from src.common.model_manager import BaseModelManager
from src.settings import Settings
from src.common.postgres import SessionLocal


class UserManager(BaseModelManager[User]):
    __model__ = User

    @classmethod
    def create_user(
        cls,
        db: Session,
        email: str,
        password: str,
        is_admin: bool,
    ) -> User:
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        user = User(
            email=email,
            password=hashed_password,
            is_admin=is_admin,
        )

        return cls.create(db, user)
    
    @classmethod
    def create_super_user(cls):
        settings = Settings()
        db = SessionLocal()
        return cls.create_user(
            db,
            settings.admin_email,
            settings.admin_password,
            is_admin=True,
        )