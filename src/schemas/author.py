import datetime

from asyncpg.pgproto.pgproto import timedelta
from pydantic import BaseModel, ConfigDict, constr, field_validator


class AuthorCreateRequest(BaseModel):
    name: str = constr(min_length=1)
    surname: str = constr(min_length=1)
    birthdate: datetime.date

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate(cls, birthdate: datetime.date) -> datetime.date:
        today = datetime.date.today()
        min_age_years = 16
        max_age_years = 120
        if today - timedelta(days=min_age_years * 365) < birthdate or birthdate < today - timedelta(
            days=max_age_years * 365
        ):
            raise ValueError("Incorrect birthdate.")
        return birthdate


class AuthorResponse(BaseModel):
    name: str
    surname: str
    birthdate: datetime.date

    model_config = ConfigDict(from_attributes=True)
