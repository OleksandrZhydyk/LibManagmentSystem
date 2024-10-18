import datetime

from pydantic import BaseModel, ConfigDict, constr, field_validator


class PublisherCreateRequest(BaseModel):
    name: str = constr(min_length=2)
    established_year: int

    @field_validator("established_year")
    @classmethod
    def validate_established_year(cls, established_year: int) -> datetime.date:
        if established_year < 1:
            raise ValueError("Year must be a positive integer.")
        if established_year > datetime.date.today().year:
            raise ValueError("Established year must not be in the future.")
        return datetime.date(established_year, 1, 1)


class PublisherResponse(BaseModel):
    id: int
    name: str
    established_year: datetime.date

    model_config = ConfigDict(from_attributes=True)
