import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class BookCreateRequest(BaseModel):
    title: str
    description: str
    isbn: str
    publish_date: datetime.date
    quantity: int = 1
    authors: list[str]
    genre: str
    publisher: str

    @field_validator("publish_date")
    @classmethod
    def validate_publish_date(cls, publish_date: datetime.date) -> datetime.date:
        if publish_date >= datetime.date.today():
            raise ValueError("Publish date can not be in the future.")
        return publish_date

    @field_validator("genre")
    @classmethod
    def validate_genre(cls, genre: str) -> str:
        return genre.lower()

    @field_validator("isbn")
    @classmethod
    def validate_isbn(cls, isbn) -> str:
        isbn = isbn.replace("-", "").replace(" ", "")

        if len(isbn) not in [10, 13]:
            raise ValueError("Incorrect length of ISBN.")

        if len(isbn) == 10 and cls.validate_isbn_10(isbn):
            return isbn
        elif len(isbn) == 13 and cls.validate_isbn_13(isbn):
            return isbn
        raise ValueError(f"Incorrect ISBN {isbn}.")

    @classmethod
    def validate_isbn_10(cls, isbn: str) -> bool:
        total = 0
        for i in range(9):
            total += int(isbn[i]) * (i + 1)

        checksum = total % 11
        if isbn[-1] == "X":
            return checksum == 10
        else:
            return checksum == int(isbn[-1])

    @classmethod
    def validate_isbn_13(cls, isbn: str) -> bool:
        total = 0
        for i in range(12):
            if i % 2 == 0:
                total += int(isbn[i]) * 1
            else:
                total += int(isbn[i]) * 3

        checksum = (10 - (total % 10)) % 10
        return checksum == int(isbn[-1])


class BookResponse(BaseModel):
    id: int
    title: str
    description: str
    isbn: str
    publish_date: datetime.date

    model_config = ConfigDict(from_attributes=True)
