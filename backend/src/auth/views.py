from http import HTTPStatus
from uuid import uuid4

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.auth.core import (
    close_user_session,
    create_user_session,
    get_authorized_user_details,
    is_authorized,
    validate_credentials,
)
from src.auth.models import Credentials, UserDetailsResponse
from src.common.exceptions import ForbiddenException, UnauthorizedException
from src.common.postgres import get_db_session

router = APIRouter()


@router.post("/login")
async def login(
    credentials: Credentials, db_session: Session = Depends(get_db_session)
) -> JSONResponse:
    user_id = validate_credentials(db_session, credentials.email, credentials.password)
    if not user_id:
        raise UnauthorizedException

    session_id = str(uuid4())
    create_user_session(db_session, user_id, session_id)
    response = JSONResponse(
        content={"status": "Logged in successfully."}, status_code=HTTPStatus.OK
    )
    response.set_cookie(key="session_id", value=session_id)
    return response


@router.post("/logout")
async def logout(
    request: Request, db_session: Session = Depends(get_db_session)
) -> JSONResponse:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise ForbiddenException
    if not close_user_session(db_session, session_id):
        raise UnauthorizedException

    response = JSONResponse(
        content={"status": "Logged out successfully"}, status_code=HTTPStatus.OK
    )
    response.delete_cookie(key="session_id")
    return response


@router.get("/my_account", dependencies=[Depends(is_authorized)])
async def my_account(
    request: Request, db_session: Session = Depends(get_db_session)
) -> UserDetailsResponse:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise ForbiddenException
    current_user = get_authorized_user_details(db_session, session_id)
    return UserDetailsResponse(email=current_user.email, is_admin=current_user.is_admin)
