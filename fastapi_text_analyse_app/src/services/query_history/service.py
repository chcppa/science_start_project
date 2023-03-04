from fastapi import Depends

from orm.database import Session, get_session
from orm.models import (FirstModeQueryInDatabase,
                        SecondModeQueryInDatabase,
                        ThirdModeQueryInDatabase
                        )
from orm.tables import SecondModeQueryTable, FirstModeQueryTable, ThirdModeQueryTable
from repositories import FirstModeQueryRepository, UnitOfWork, SecondModeQueryRepository, ThirdModeQueryRepository


class QueryHistoryService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_first_mode_query(self, query_data: dict) -> FirstModeQueryInDatabase:
        parsed_query = FirstModeQueryInDatabase(**query_data)
        new_query = FirstModeQueryTable(id=None, **parsed_query.dict())
        repo = FirstModeQueryRepository()

        with UnitOfWork(session_obj=self.session, repos_list=[repo]) as uow:
            uow.set_repos_session()
            repo.save_query(new_query)

        return parsed_query

    def create_second_mode_query(self, query_data: dict) -> SecondModeQueryInDatabase:
        parsed_query = SecondModeQueryInDatabase(**query_data)
        new_query = SecondModeQueryTable(id=None, **parsed_query.dict())
        repo = SecondModeQueryRepository()

        with UnitOfWork(session_obj=self.session, repos_list=[repo]) as uow:
            uow.set_repos_session()
            repo.save_query(new_query)

        return parsed_query

    def create_third_mode_query(self, query_data: dict) -> ThirdModeQueryInDatabase:
        parsed_query = ThirdModeQueryInDatabase(**query_data)
        new_query = ThirdModeQueryTable(id=None, **parsed_query.dict())
        repo = ThirdModeQueryRepository()

        with UnitOfWork(session_obj=self.session, repos_list=[repo]) as uow:
            uow.set_repos_session()
            repo.save_query(new_query)

        return parsed_query

    def get_all_first_mode_queries(self, user_id: int) -> list[FirstModeQueryInDatabase]:
        repo = FirstModeQueryRepository(self.session)
        return list(map(lambda x: FirstModeQueryInDatabase.from_orm(x[0]), repo.get_all_by_user_id(user_id)))

    def get_the_first_mode_query(self, user_id: int) -> FirstModeQueryInDatabase:
        repo = FirstModeQueryRepository(self.session)
        return repo.get_by_user_id(user_id)

    def get_all_second_mode_queries(self, user_id: int) -> list[SecondModeQueryInDatabase]:
        repo = SecondModeQueryRepository(self.session)
        return list(map(lambda x: SecondModeQueryInDatabase.from_orm(x[0]), repo.get_all_by_user_id(user_id)))

    def get_the_second_mode_query(self, user_id: int) -> SecondModeQueryInDatabase:
        repo = SecondModeQueryRepository(self.session)
        return repo.get_by_user_id(user_id)

    def get_all_third_mode_queries(self, user_id: int) -> list[ThirdModeQueryInDatabase]:
        repo = ThirdModeQueryRepository(self.session)
        return list(map(lambda x: ThirdModeQueryInDatabase.from_orm(x[0]), repo.get_all_by_user_id(user_id)))

    def get_the_third_mode_query(self, user_id: int) -> ThirdModeQueryInDatabase:
        repo = ThirdModeQueryRepository(self.session)
        return repo.get_by_user_id(user_id)
