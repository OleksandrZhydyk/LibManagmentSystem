from pydantic import BaseModel, constr, field_validator


class GenreCreateRequest(BaseModel):
    name: str = constr(min_length=2)

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        return name.lower()


class GenreCreateResponse(BaseModel):
    name: str = constr(min_length=2)
