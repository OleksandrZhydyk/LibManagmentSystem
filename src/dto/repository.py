from collections.abc import Sequence
from dataclasses import dataclass

from database.models import Author


@dataclass(slots=True, frozen=True)
class SearchFieldDTO:
    column: str
    value: str | int | bool | list | None
    operator: str = "__eq__"


@dataclass(slots=True, frozen=True)
class AuthorsExistDTO:
    found_authors: Sequence[Author]
    missing_authors: list[str]
