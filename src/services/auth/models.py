from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None


class BaseUser(BaseModel):
    username: str


class UserCreate(BaseUser):
    password: str


class UserInDatabase(BaseUser):
    registration_date: datetime
    hashed_password: str
