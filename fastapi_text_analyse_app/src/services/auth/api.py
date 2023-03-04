from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from services.auth.models import Token, UserCreate
from services.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-up", response_model=Token, status_code=status.HTTP_201_CREATED)
def sign_up(user: UserCreate, auth_service: AuthService = Depends(AuthService)):
    return auth_service.create_user(user.dict())


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          auth_service: AuthService = Depends(AuthService)):
    return auth_service.authenticate_user(form_data.username, form_data.password)
