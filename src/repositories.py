from abc import ABC, abstractmethod
from typing import Sequence

from sqlalchemy import select, Row, delete
from sqlalchemy.orm import Session

from orm.tables import (
    UserTable,
    FirstModeQueryTable,
    SecondModeQueryTable,
    ThirdModeQueryTable
)


class BaseRepository:

    def __init__(self, session_obj: Session = None):
        """
        Repositories can set up a session on their own.
        """
        if session_obj is not None:
            self.__session = session_obj

    def set_session(self, session_obj: Session):
        """
        The repository session can be managed by Unit Of Work.
        """
        self.__session = session_obj

    def get_session(self) -> Session:
        return self.__session

    session = property(get_session, set_session)


class UnitOfWork:

    def __init__(self, session_obj: Session, repos_list):
        self.repos_list = repos_list
        self.session = session_obj

    def set_repos_session(self) -> None:
        """
        Set up a session for linked repositories.
        """
        for repo in self.repos_list:
            repo.session = self.session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.session.rollback()
        else:
            self.session.commit()


class UserRepository(BaseRepository):
    """Repo for user database actions."""

    def save(self, user: UserTable) -> None:
        self.session.add(user)

    def get_by_username(self, username: str):
        user = self.session.execute(
            select(UserTable).filter(UserTable.username == username)
        ).scalar()

        return user

    def get_by_user_id(self, user_id: int):
        user = self.session.execute(
            select(UserTable).filter(UserTable.id == user_id)
        ).scalar()

        return user

    def get_users(self) -> Sequence[Row]:
        users = self.session.execute(
            select(UserTable)
        ).all()

        return users

    def delete_by_user_id(self, user_id: int) -> None:
        self.session.execute(
            delete(UserTable)
            .where(UserTable.id == user_id))


class BaseModeQueryRepository(ABC, BaseRepository):
    """Base repo for analysis modes databases actions."""

    def save_query(
            self,
            query
    ) -> None:
        self.session.add(query)

    @abstractmethod
    def get_by_user_id(self, user: UserTable):
        raise NotImplementedError

    @abstractmethod
    def get_all_by_user_id(self, user: UserTable):
        raise NotImplementedError


class FirstModeQueryRepository(BaseModeQueryRepository):
    """Repo for first analysis mode database actions."""

    def get_by_user_id(self, user_id: int) -> FirstModeQueryTable:
        query = self.session.execute(
            select(FirstModeQueryTable).filter(FirstModeQueryTable.user_id == user_id)
        ).scalar()

        return query

    def get_all_by_user_id(self, user_id: int) -> Sequence[Row]:
        queries = self.session.execute(
            select(FirstModeQueryTable).filter(FirstModeQueryTable.user_id == user_id)
        ).all()

        return queries


class SecondModeQueryRepository(BaseModeQueryRepository):
    """Repo for second analysis mode database actions."""

    def get_by_user_id(self, user_id: int) -> SecondModeQueryTable:
        query = self.session.execute(
            select(SecondModeQueryTable).filter(FirstModeQueryTable.user_id == user_id)
        ).scalar()

        return query

    def get_all_by_user_id(self, user_id: int) -> Sequence[Row]:
        queries = self.session.execute(
            select(SecondModeQueryTable).filter(SecondModeQueryTable.user_id == user_id)
        ).all()

        return queries


class ThirdModeQueryRepository(BaseModeQueryRepository):
    """Repo for third analysis mode database actions."""

    def get_by_user_id(self, user_id: int) -> ThirdModeQueryTable:
        query = self.session.execute(
            select(ThirdModeQueryTable).filter(ThirdModeQueryTable.user_id == user_id)
        ).scalar()

        return query

    def get_all_by_user_id(self, user_id: int) -> Sequence[Row]:
        queries = self.session.execute(
            select(ThirdModeQueryTable).filter(ThirdModeQueryTable.user_id == user_id)
        ).all()

        return queries
