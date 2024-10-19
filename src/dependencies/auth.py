from database.models import User
from dependencies.service import get_auth_service
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from schemas.user import UserResponse
from security import bearer_scheme, decode_jwt
from services.auth import AuthService
from starlette import status

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "authenticate_value"},
)


def get_token_payload(token: str) -> dict:
    try:
        payload = decode_jwt(token)
    except ValueError as e:
        raise credentials_exception from e
    return payload


async def get_user(email: str, service) -> User:
    user = await service.get_user(email)
    if user is None:
        raise credentials_exception
    return user


def get_user_identifier(payload: dict, identifier_key: str) -> str | int:
    identifier = payload.get(identifier_key)
    if identifier is None:
        raise credentials_exception
    return identifier


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(bearer_scheme), service: AuthService = Depends(get_auth_service)
):
    token: str = token.credentials
    payload = get_token_payload(token)
    email = get_user_identifier(payload, "email")
    return await get_user(email, service)


async def get_current_active_user(current_user: UserResponse = Security(get_current_user)) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
