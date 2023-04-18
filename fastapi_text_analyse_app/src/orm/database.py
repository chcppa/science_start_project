from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SessionType

from settings import settings

db = f"{settings.db_url}chcppa:ZMBa83sYJ2xm9fMk5FwMnh4lWGqhaA22@dpg-cgume7539el96k1vca70-a.frankfurt-postgres.render.com/database_45be" #f"{settings.db_url}{settings.db_user}:{settings.db_password}@{settings.db_host}/{settings.db_name}"
engine = create_engine(db, echo=False)
Session = sessionmaker(bind=engine, autocommit=False)


def get_session() -> SessionType:
    """
    External dependency, return db session.
    """
    session = Session()
    try:
        yield session
    finally:
        session.close()
