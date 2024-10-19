import datetime

import pytest
from pydantic import ValidationError
from schemas.author import AuthorCreateRequest
from schemas.book import BookCreateRequest
from schemas.borrows import BorrowCreateRequest
from schemas.publisher import PublisherCreateRequest, min_established_year
from schemas.user import UserCreateRequest


def test_author_creation_success(create_author):
    author = AuthorCreateRequest(**create_author)
    assert isinstance(author, AuthorCreateRequest)
    assert isinstance(author.birthdate, datetime.date)
    assert author.birthdate == datetime.date(1995, 1, 1)


def test_author_incorrect_birthdate_failure(create_author):
    today_date = datetime.date.today()
    create_author["birthdate"] = today_date

    with pytest.raises(ValidationError) as exc_info:
        AuthorCreateRequest(**create_author)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == [
        {
            "type": "value_error",
            "loc": ("birthdate",),
            "msg": "Value error, Incorrect birthdate, birthdate can not be today or in " "future.",
            "input": today_date,
        },
    ]


def test_book_creation_success(create_book):
    book = BookCreateRequest(**create_book)
    assert isinstance(book, BookCreateRequest)
    assert isinstance(book.publish_date, datetime.date)
    assert book.title == "Book 1"


def test_book_creation_with_isbn_x_end_success(create_book):
    create_book["isbn"] = "1-55404-295-X"
    book = BookCreateRequest(**create_book)
    assert isinstance(book, BookCreateRequest)
    assert isinstance(book.publish_date, datetime.date)
    assert book.isbn == "155404295X"


def test_book_incorrect_publish_date_failure(create_book):
    today_date = datetime.date.today()
    create_book["publish_date"] = today_date

    with pytest.raises(ValidationError) as exc_info:
        BookCreateRequest(**create_book)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == [
        {
            "type": "value_error",
            "loc": ("publish_date",),
            "msg": "Value error, Publish date can not be in the future.",
            "input": today_date,
        },
    ]


@pytest.mark.parametrize(
    "book_data, expected_error_msg",
    (
        (
            {"isbn": "123456"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect length of ISBN.",
                    "input": "123456",
                }
            ],
        ),
        (
            {"isbn": "123-456-78912-345"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect length of ISBN.",
                    "input": "123-456-78912-345",
                }
            ],
        ),
        (
            {"isbn": "978-0-306-40615-8"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect ISBN 9780306406158.",
                    "input": "978-0-306-40615-8",
                }
            ],
        ),
        (
            {"isbn": "1-56619-909-4"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect ISBN 1566199094.",
                    "input": "1-56619-909-4",
                }
            ],
        ),
    ),
)
def test_book_incorrect_isbn_failure(create_book, book_data, expected_error_msg):
    create_book.update(book_data)
    with pytest.raises(ValidationError) as exc_info:
        BookCreateRequest(**create_book)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == expected_error_msg


@pytest.mark.parametrize(
    "book_data, expected_error_msg",
    (
        (
            {"isbn": "123456"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect length of ISBN.",
                    "input": "123456",
                }
            ],
        ),
        (
            {"isbn": "123-456-78912-345"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect length of ISBN.",
                    "input": "123-456-78912-345",
                }
            ],
        ),
        (
            {"isbn": "978-0-306-40615-8"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect ISBN 9780306406158.",
                    "input": "978-0-306-40615-8",
                }
            ],
        ),
        (
            {"isbn": "1-56619-909-4"},
            [
                {
                    "type": "value_error",
                    "loc": ("isbn",),
                    "msg": "Value error, Incorrect ISBN 1566199094.",
                    "input": "1-56619-909-4",
                }
            ],
        ),
    ),
)
def test_borrow_incorrect_isbn_failure(book_data, expected_error_msg):
    with pytest.raises(ValidationError) as exc_info:
        BorrowCreateRequest(**book_data)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == expected_error_msg


def test_publisher_creation_success(create_publisher):
    publisher = PublisherCreateRequest(**create_publisher)
    assert isinstance(publisher, PublisherCreateRequest)
    assert isinstance(publisher.established_year, datetime.date)
    assert publisher.name == "Publisher 1"


@pytest.mark.parametrize(
    "publisher_data, expected_error_msg",
    (
        (
            {"established_year": datetime.date.today().year + 1},
            [
                {
                    "type": "value_error",
                    "loc": ("established_year",),
                    "msg": "Value error, Established year can not be in the future.",
                    "input": datetime.date.today().year + 1,
                }
            ],
        ),
        (
            {"established_year": 999},
            [
                {
                    "type": "value_error",
                    "loc": ("established_year",),
                    "msg": f"Value error, Established year can not be older than {min_established_year}.",
                    "input": 999,
                }
            ],
        ),
    ),
)
def test_publisher_incorrect_established_year_failure(create_publisher, publisher_data, expected_error_msg):
    create_publisher.update(publisher_data)
    with pytest.raises(ValidationError) as exc_info:
        PublisherCreateRequest(**create_publisher)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == expected_error_msg


def test_user_creation_success(create_user):
    user = UserCreateRequest(**create_user)
    assert isinstance(user, UserCreateRequest)
    assert user.password != "password"
    assert user.name == "User 1"


def test_user_passwords_compare_failure(create_user):
    create_user["confirmed_password"] = "not equal password"
    with pytest.raises(ValidationError) as exc_info:
        UserCreateRequest(**create_user)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == [
        {
            "type": "value_error",
            "loc": ("confirmed_password",),
            "msg": "Value error, Please enter the same value for password and confirmation password field.",
            "input": "not equal password",
        }
    ]


def test_user_password_length_failure(create_user):
    create_user["password"] = "pass"
    with pytest.raises(ValidationError) as exc_info:
        UserCreateRequest(**create_user)
    errors = exc_info.value.errors(include_url=False)
    [error.pop("ctx", None) for error in errors]
    assert errors == [
        {
            "type": "string_too_short",
            "loc": ("password",),
            "msg": "String should have at least 8 characters",
            "input": "pass",
        }
    ]
