from dataclasses import asdict

from dependencies.service import get_auth_service
from fastapi import APIRouter, Depends, HTTPException
from schemas.auth import AccessToken, UserLogin
from schemas.exception import HTTPExceptionResponse
from schemas.user import UserCreate
from security import set_cookie_to_response
from services.auth import AuthService
from starlette.responses import Response

router = APIRouter()


@router.post(
    "/register",
    response_model=AccessToken,
    responses={409: {"model": HTTPExceptionResponse, "description": "User already exists."}},
)
async def register(
    response: Response,
    user_create: UserCreate,
    service: AuthService = Depends(get_auth_service),
):
    try:
        tokens = await service.register(user_create)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    set_cookie_to_response(response, "refresh", tokens.refresh)
    return AccessToken(**asdict(tokens))


@router.post(
    "/login",
    response_model=AccessToken,
    responses={401: {"model": HTTPExceptionResponse, "description": "Incorrect user credentials provided."}},
)
async def login(response: Response, user_creds: UserLogin, service: AuthService = Depends(get_auth_service)):
    try:
        tokens = await service.login(user_creds)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e

    set_cookie_to_response(response, "refresh", tokens.refresh)
    return AccessToken(**asdict(tokens))
