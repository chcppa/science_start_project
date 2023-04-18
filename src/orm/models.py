from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserInDatabase(BaseModel):
    username: str
    hashed_password: str
    registration_date: date = Field(description="Registration date in UTC.")

    class Config:
        orm_mode = True


class BaseQuery(BaseModel):
    original_text: str = Field(description="The original text of the request.")

    class Config:
        orm_mode = True

    query_date: datetime = Field(description="Request date in UTC.")


class FirstModeQuery(BaseQuery):
    confidence_score: int = Field(description="The level of coincidence as a percentage.")
    tag: str = Field(description="Text subject")


class FirstModeQueryInDatabase(FirstModeQuery):
    user_id: int


class SecondModeQuery(BaseQuery):
    negative: Optional[int]
    neutral: Optional[int]
    positive: Optional[int]
    angry: Optional[int]
    sad: Optional[int]
    excited: Optional[int]
    bored: Optional[int]
    happy: Optional[int]
    fear: Optional[int]


class SecondModeQueryInDatabase(SecondModeQuery):
    user_id: int


class ThirdModeQuery(BaseQuery):
    abusive: int
    hate_speech: int
    neither: int
    angry: Optional[int]
    sad: Optional[int]
    excited: Optional[int]
    bored: Optional[int]
    happy: Optional[int]
    fear: Optional[int]


class ThirdModeQueryInDatabase(ThirdModeQuery):
    user_id: int
