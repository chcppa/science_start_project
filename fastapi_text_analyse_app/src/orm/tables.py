from datetime import datetime

from sqlalchemy import (
    ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column

Base = declarative_base()


class UserTable(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    registration_date: Mapped[datetime]


class FirstModeQueryTable(Base):
    __tablename__ = "query_1"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    confidence_score: Mapped[int]
    tag: Mapped[str]
    query_date: Mapped[datetime]

    original_text: Mapped[str]

    user: Mapped["UserTable"] = relationship(lazy="selectin")


class SecondModeQueryTable(Base):
    __tablename__ = "query_2"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    negative: Mapped[int] = mapped_column(nullable=True)
    neutral: Mapped[int] = mapped_column(nullable=True)
    positive: Mapped[int] = mapped_column(nullable=True)
    angry: Mapped[int] = mapped_column(nullable=True)
    sad: Mapped[int] = mapped_column(nullable=True)
    excited: Mapped[int] = mapped_column(nullable=True)
    bored: Mapped[int] = mapped_column(nullable=True)
    happy: Mapped[int] = mapped_column(nullable=True)
    fear: Mapped[int] = mapped_column(nullable=True)

    query_date: Mapped[datetime]

    original_text: Mapped[str]

    user: Mapped["UserTable"] = relationship(lazy="selectin")


class ThirdModeQueryTable(Base):
    __tablename__ = "query_3"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    abusive: Mapped[int] = mapped_column(nullable=True)
    hate_speech: Mapped[int] = mapped_column(nullable=True)
    neither: Mapped[int] = mapped_column(nullable=True)
    angry: Mapped[int] = mapped_column(nullable=True)
    sad: Mapped[int] = mapped_column(nullable=True)
    excited: Mapped[int] = mapped_column(nullable=True)
    bored: Mapped[int] = mapped_column(nullable=True)
    happy: Mapped[int] = mapped_column(nullable=True)
    fear: Mapped[int] = mapped_column(nullable=True)

    query_date: Mapped[datetime]

    original_text: Mapped[str]

    user: Mapped["UserTable"] = relationship(lazy="selectin")
