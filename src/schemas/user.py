from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, constr, model_validator
from pydantic_core.core_schema import ValidationInfo
from security import hash_password


def ensure_passwords_match(v: str, info: ValidationInfo) -> str:
    if "password" in info.data and v != info.data["password"]:
        raise ValueError("Please enter the same value for password and confirmation password field.")
    return v


class UserCreateRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: constr(min_length=8)
    confirmed_password: Annotated[str, AfterValidator(ensure_passwords_match)]

    @model_validator(mode="after")
    @classmethod
    def post_update(cls, user):
        user.password = hash_password(user.password)
        return user


class UserResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)
