from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# 伪用户数据库
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


# 伪哈希函数
def fakely_hash_password(password: str):
    return f"hashed{password}"


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


# 从伪数据库中查找用户
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


# 伪令牌生成
def fake_token_generator(user: UserInDB) -> str:
    return f"tokenized{user.username}"


# 伪令牌解析
def fake_token_resolver(token: str) -> UserInDB | None:
    if token.startswith("tokenized"):
        user_id = token.removeprefix("tokenized")
        user = get_user(fake_users_db, user_id)
        return user


# 客户端需要在/token端点 进行身份验证并获取Bearer令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 通过令牌获取用户
def get_user_from_token(token: str = Depends(oauth2_scheme)) -> UserInDB:
    user = fake_token_resolver(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
