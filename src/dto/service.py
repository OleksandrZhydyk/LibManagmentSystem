from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class TokenDTO:
    access: str
    refresh: str
