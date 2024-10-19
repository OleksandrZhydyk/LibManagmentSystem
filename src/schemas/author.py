import datetime

from pydantic import BaseModel, ConfigDict, constr, field_validator


class AuthorCreateRequest(BaseModel):
    name: str = constr(min_length=1)
    surname: str = constr(min_length=1)
    birthdate: datetime.date

    @field_validator("birthdate")
    @classmethod
    def validate_birthdate(cls, birthdate: datetime.date) -> datetime.date:
        today_date = datetime.date.today()
        if birthdate >= today_date:
            raise ValueError("Incorrect birthdate, birthdate can not be today or in future.")
        return birthdate


class AuthorResponse(BaseModel):
    name: str
    surname: str
    birthdate: datetime.date

    model_config = ConfigDict(from_attributes=True)
