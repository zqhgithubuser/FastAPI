from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from db_connection import get_session
from models import Role
from security import decode_access_token, oauth2_scheme


class UserCreateResquestWithRole(BaseModel):
    username: str
    email: EmailStr
    role: Role


def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> UserCreateResquestWithRole:
    user = decode_access_token(token, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return UserCreateResquestWithRole(
        username=user.username, email=user.email, role=user.role
    )


def get_premium_user(current_user: Annotated[get_current_user, Depends()]):
    if current_user.role != Role.premium:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authorized",
        )
    return current_user


router = APIRouter()


@router.get(
    "/welcome/all-users",
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "User not authorized"}},
)
def all_users_can_access(user: Annotated[get_current_user, Depends()]):
    return {f"Hello {user.username}, welcome to your space"}


@router.get(
    "/welcome/premium-user",
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "User not authorized"}},
)
def only_premium_users_can_access(
    user: UserCreateResquestWithRole = Depends(get_premium_user),
):
    return {f"Hello {user.username}, Welcome to your premium space"}
