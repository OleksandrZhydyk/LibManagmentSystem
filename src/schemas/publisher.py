import datetime

from pydantic import BaseModel, ConfigDict, constr, field_validator

min_established_year: int = 1000


class PublisherCreateRequest(BaseModel):
    name: str = constr(min_length=2)
    established_year: int

    @field_validator("established_year")
    @classmethod
    def validate_established_year(cls, established_year: int) -> datetime.date:
        if established_year < min_established_year:
            raise ValueError(f"Established year can not be older than {min_established_year}.")
        if established_year > datetime.date.today().year:
            raise ValueError("Established year can not be in the future.")
        return datetime.date(established_year, 1, 1)


class PublisherResponse(BaseModel):
    id: int
    name: str
    established_year: datetime.date

    model_config = ConfigDict(from_attributes=True)
