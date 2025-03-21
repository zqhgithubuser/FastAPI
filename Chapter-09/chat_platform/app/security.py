from fastapi import APIRouter, Depends, HTTPException, WebSocketException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.ws_password_bearer import OAuth2WebSocketPasswordBearer

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "hashed_password": "hashedsecret",
    },
    "janedoe": {
        "username": "janedoe",
        "hashed_password": "hashedsecret2",
    },
}


def fakely_hash_password(password: str):
    return f"hashed{password}"


class User(BaseModel):
    username: str


def get_user(db: dict[str, str], username: str) -> User | None:
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def fake_token_generator(username: str) -> str:
    return f"tokenized{username}"


def fake_token_resolver(
    token: str,
) -> User | None:
    if token.startswith("tokenized"):
        user_id = token.removeprefix("tokenized")
        user = get_user(fake_users_db, user_id)
        return user


oauth2_scheme_for_ws = OAuth2WebSocketPasswordBearer(tokenUrl="/token")


def get_username_from_token(
    token: str = Depends(oauth2_scheme_for_ws),
) -> str:
    user = fake_token_resolver(token)
    if not user:
        raise WebSocketException(
            code=status.HTTP_401_UNAUTHORIZED,
            reason="Invalid authentication credentials",
        )
    return user.username


router = APIRouter()


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )
    hashed_password = fakely_hash_password(form_data.password)
    if not hashed_password == user_dict.get("hashed_password"):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    token = fake_token_generator(form_data.username)

    return {
        "access_token": token,
        "token_type": "bearer",
    }
