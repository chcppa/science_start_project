from datetime import timedelta, datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from orm.database import get_session
from orm.tables import UserTable
from repositories import UserRepository, UnitOfWork
from services.auth.exceptions import InvalidTokenError, AuthenticateError, UsernameValidationError
from services.auth.models import UserInDatabase, Token
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    return AuthService.verify_token(token)


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @staticmethod
    def create_access_token(user_id: int) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(seconds=settings.jwt_expires_s),
            'user_id': str(user_id)
        }

        encoded_jwt = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> int:
        try:
            payload = jwt.decode(
                token,
                settings.jwt_secret,
                algorithms=[settings.jwt_algorithm],
            )
        except JWTError:
            raise InvalidTokenError from None

        user_id = payload.get('user_id')
        print(user_id)
        return user_id

    def validate_username(self, username: str) -> bool:
        user_repo = UserRepository(self.session)

        if user_repo.get_by_username(username) is None:
            return True
        return False

    def create_user(self, user_data: dict) -> Token:
        if not self.validate_username(username=user_data["username"]):
            raise UsernameValidationError from None

        user = UserInDatabase(
            username=user_data["username"],
            registration_date=datetime.utcnow(),
            hashed_password=self.get_password_hash(user_data["password"])
        )

        user_repo = UserRepository()

        with UnitOfWork(self.session, repos_list=[user_repo]) as uow:
            uow.set_repos_session()
            user_repo.save(UserTable(id=None, **user.dict()))

        token = self.authenticate_user(user_data["username"], user_data["password"])
        return token

    def authenticate_user(self, username: str, password: str) -> Token:
        user_repo = UserRepository(self.session)
        user = user_repo.get_by_username(username)

        if not user:
            raise AuthenticateError

        if not self.verify_password(password, user.hashed_password):
            raise AuthenticateError

        return Token(access_token=self.create_access_token(user.id), token_type="bearer")
