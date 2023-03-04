from datetime import datetime

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class BaseUser(BaseModel):
    username: str


class UserCreate(BaseUser):
    password: str


class UserInDatabase(BaseUser):
    registration_date: datetime
    hashed_password: str
