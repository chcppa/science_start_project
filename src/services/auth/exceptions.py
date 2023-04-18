from fastapi import HTTPException
from starlette import status

UsernameValidationError = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Username already use')

InvalidTokenError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'})

AuthenticateError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"})
