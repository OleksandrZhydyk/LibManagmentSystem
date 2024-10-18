from pydantic import BaseModel, EmailStr


class AccessToken(BaseModel):
    access: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
