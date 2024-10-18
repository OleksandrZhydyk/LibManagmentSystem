import datetime

import jwt
from config import conf
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from starlette.responses import Response

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def sign_jwt(payload: dict, expiration_time: int | None = None) -> str:
    exp = datetime.datetime.now(datetime.UTC) + datetime.timedelta(seconds=expiration_time) if expiration_time else None
    return jwt.encode({**payload, "exp": exp}, conf.JWT_SECRET, algorithm=conf.JWT_ALGORITHM)


def decode_jwt(token: str) -> dict:
    try:
        return jwt.decode(
            jwt=token,
            key=conf.JWT_SECRET,
            algorithms=[conf.JWT_ALGORITHM],
            verify_expiration=True,
        )
    except jwt.ExpiredSignatureError as e:
        raise ValueError("Token expired try to registrate again") from e
    except jwt.InvalidTokenError as e:
        raise ValueError("Invalid token") from e


def set_cookie_to_response(response: Response, name: str, value: str, expires: int | None = None) -> Response:
    if expires:
        expires = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=expires)
    response.set_cookie(
        name,
        value,
        httponly=conf.AUTH_COOKIE_HTTPONLY,
        secure=conf.AUTH_COOKIE_SECURE,
        samesite=conf.AUTH_COOKIE_SAME_SITE,
        expires=expires,
    )
    return response
