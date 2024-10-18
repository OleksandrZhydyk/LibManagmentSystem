import datetime

from pydantic import BaseModel, ConfigDict, field_validator, model_validator


class BorrowCreateRequest(BaseModel):
    isbn: str

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


class BookReturnRequest(BorrowCreateRequest):
    pass


class BorrowResponse(BaseModel):
    book_name: str
    book_isbn: str
    borrow_date: datetime.date
    return_date: datetime.date
    borrower_name: str | None
    borrower_surname: str | None
    returned: bool

    @model_validator(mode="before")
    def set_returned(self):
        self.returned = bool(self.return_date)
        return self

    model_config = ConfigDict(from_attributes=True)
