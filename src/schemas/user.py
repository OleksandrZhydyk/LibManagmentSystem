from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr
from pydantic_core.core_schema import ValidationInfo
from security import hash_password


def ensure_passwords_match(v: str, info: ValidationInfo) -> str:
    if "confirmed_password" in info.data and v != info.data["confirmed_password"]:
        raise ValueError("Please enter the same value for password and confirmation password field.")
    return v


def get_hashed_password(v: str, info: ValidationInfo) -> str:
    password = ensure_passwords_match(v, info)
    return hash_password(password)


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: Annotated[str, AfterValidator(get_hashed_password)]
    confirmed_password: str


class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
