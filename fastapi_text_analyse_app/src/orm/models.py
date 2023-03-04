from datetime import date, datetime

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
    negative: int | None
    neutral: int | None
    positive: int | None
    angry: int | None
    sad: int | None
    excited: int | None
    bored: int | None
    happy: int | None
    fear: int | None


class SecondModeQueryInDatabase(SecondModeQuery):
    user_id: int


class ThirdModeQuery(BaseQuery):
    abusive: int
    hate_speech: int
    neither: int
    angry: int | None
    sad: int | None
    excited: int | None
    bored: int | None
    happy: int | None
    fear: int | None


class ThirdModeQueryInDatabase(ThirdModeQuery):
    user_id: int
