from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, Request
from sqlalchemy.orm import Session
from src.auth.repositories import UserRepository, UserSessionRepository
from src.common.exceptions import ForbiddenException, UnauthorizedException
from src.common.postgres import get_db_session
from src.config import TZ_INFO, USER_SESSION_DURATION_DAYS
from src.models.user import User


def validate_credentials(db_session: Session, email: str, password: str) -> int:
    user = UserRepository.find_first_by_value(db_session, "email", email)
    if not user:
        raise ForbiddenException
    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        raise UnauthorizedException
    return user.id


def create_user_session(db_session: Session, user_id: int, user_session_id: str) -> int:
    expiration_datetime = datetime.now() + timedelta(days=USER_SESSION_DURATION_DAYS)
    user_session = UserSessionRepository.create_session(
        db_session, user_id, user_session_id, expiration_datetime
    )
    return user_session.id


def close_user_session(db_session: Session, user_session_id: str) -> bool:
    user_session = UserSessionRepository.find_first_by_value(
        db_session, "session_id", user_session_id
    )
    if not user_session:
        return False

    UserSessionRepository.delete(db_session, user_session)
    return True


def get_authorized_user_details(db_session: Session, user_session_id: str) -> User:
    user_session = UserSessionRepository.find_first_by_value(
        db_session, "session_id", user_session_id
    )

    session_expiration_datetime: datetime = user_session.expiration_datetime

    if not user_session or session_expiration_datetime < datetime.now():
        raise UnauthorizedException

    return UserRepository.find_by_id(db_session, user_session.user_id)


def is_authorized(
    request: Request, db_session: Session = Depends(get_db_session)
) -> bool:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise ForbiddenException

    user_session = UserSessionRepository.find_first_by_value(
        db_session, "session_id", session_id
    )

    if not user_session:
        raise UnauthorizedException

    session_expiration_datetime: datetime = user_session.expiration_datetime

    if session_expiration_datetime < datetime.now():
        raise UnauthorizedException
    return True
