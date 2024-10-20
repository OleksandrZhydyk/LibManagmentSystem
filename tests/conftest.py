import config as app_config
import pytest
from database.models import Author
from dto.repository import AuthorsExistDTO
from pydantic_settings import BaseSettings


class TestConfig(BaseSettings):
    JWT_SECRET: str = "JWT_SECRET"
    JWT_ALGORITHM: str = "HS256"

    @property
    def DB_URL(self) -> str:
        return "sqlite+aiosqlite:///data.db"


app_config.conf = TestConfig()


@pytest.fixture(scope="function")
def create_book() -> dict:
    return {
        "title": "Book 1",
        "description": "Book 1",
        "isbn": "978-0-262-13472-9",
        "publish_date": "1995-01-01",
        "quantity": 3,
        "authors": ["Author 1"],
        "genre": "horror",
        "publisher": "Publisher 1",
    }


@pytest.fixture(scope="function")
def create_author() -> dict:
    return {"name": "Author 1", "surname": "Surname", "birthdate": "1995-01-01"}


@pytest.fixture(scope="function")
def create_publisher() -> dict:
    return {"name": "Publisher 1", "established_year": 2000}


@pytest.fixture(scope="function")
def create_genre() -> dict:
    return {
        "name": "Genre 1",
    }


@pytest.fixture(scope="function")
def create_user() -> dict:
    return {
        "name": "User 1",
        "surname": "Surname 1",
        "email": "test@test.com",
        "password": "password",
        "confirmed_password": "password",
    }


@pytest.fixture(scope="function")
def missing_authors(create_author) -> AuthorsExistDTO:
    return AuthorsExistDTO(missing_authors=["some author"], found_authors=[Author(**create_author)])


@pytest.fixture(scope="function")
def authors_presence(create_author) -> AuthorsExistDTO:
    return AuthorsExistDTO(missing_authors=[], found_authors=[Author(**create_author)])
