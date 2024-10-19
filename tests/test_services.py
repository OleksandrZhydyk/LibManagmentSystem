import pytest
from dependencies.service import (
    get_author_service,
    get_book_service,
    get_borrow_service,
    get_genre_service,
    get_publisher_service,
)
from repositories.author import AuthorRepository
from repositories.book import BookRepository
from repositories.borrows import BorrowRepository
from repositories.genre import GenreRepository
from repositories.publisher import PublisherRepository
from schemas.author import AuthorCreateRequest
from schemas.book import BookCreateRequest
from schemas.borrows import BookReturnRequest, BorrowCreateRequest
from schemas.genre import GenreCreateRequest
from schemas.publisher import PublisherCreateRequest
from schemas.user import UserCreateRequest


async def test_author_creation_uniqueness(create_author, mocker):
    mocker.patch.object(AuthorRepository, "exists", return_value=True)
    service = get_author_service(mocker.MagicMock())
    author = AuthorCreateRequest(**create_author)
    with pytest.raises(ValueError) as exc_info:
        await service.create_author(author)
    assert str(exc_info.value) == f"Author {author.name} already exists."


async def test_get_books_not_existing_author(create_author, mocker):
    mocker.patch.object(AuthorRepository, "exists", return_value=False)
    service = get_author_service(mocker.MagicMock())
    author_id = 1
    with pytest.raises(ValueError) as exc_info:
        await service.get_author_books(author_id)
    assert str(exc_info.value) == "Author doesn't exist."


async def test_publisher_creation_uniqueness(create_publisher, mocker):
    mocker.patch.object(PublisherRepository, "exists", return_value=True)
    service = get_publisher_service(mocker.MagicMock())
    publisher = PublisherCreateRequest(**create_publisher)
    with pytest.raises(ValueError) as exc_info:
        await service.create_publisher(publisher)
    assert str(exc_info.value) == f"Publisher {publisher.name} already exists."


async def test_genre_creation_uniqueness(create_genre, mocker):
    mocker.patch.object(GenreRepository, "exists", return_value=True)
    service = get_genre_service(mocker.MagicMock())
    genre = GenreCreateRequest(**create_genre)
    with pytest.raises(ValueError) as exc_info:
        await service.create_genre(genre)
    assert str(exc_info.value) == f"Genre {genre.name} already exists."


async def test_books_creation_success(create_book, mocker, authors_presence):
    mocker.patch.object(AuthorRepository, "get_authors", return_value=authors_presence)
    mocker.patch.object(BookRepository, "exists", return_value=False)
    mocker.patch.object(PublisherRepository, "get_one", return_value=True)
    mocker.patch.object(GenreRepository, "get_one", return_value=True)

    book = BookCreateRequest(**create_book)
    mocker.patch.object(BookRepository, "create", return_value=book)

    service = get_book_service(mocker.MagicMock())
    db_book = await service.create_book(book)

    assert book.title == db_book.title
    assert book.authors == db_book.authors


@pytest.mark.parametrize(
    "book_presence, author_presence, genre_presence, publisher_presence, expected_error_msg",
    (
        (True, "authors_presence", True, True, "Book ISBN 9780262134729 already exists."),
        (False, "missing_authors", True, True, "Author doesn't exist."),
        (False, "authors_presence", None, True, "Genre doesn't exist."),
        (False, "authors_presence", True, None, "Publisher doesn't exist."),
    ),
)
async def test_books_creation_failure(
    create_book, mocker, book_presence, author_presence, genre_presence, publisher_presence, expected_error_msg, request
):
    mocker.patch.object(AuthorRepository, "get_authors", return_value=request.getfixturevalue(author_presence))
    mocker.patch.object(BookRepository, "exists", return_value=book_presence)
    mocker.patch.object(PublisherRepository, "get_one", return_value=publisher_presence)
    mocker.patch.object(GenreRepository, "get_one", return_value=genre_presence)

    book = BookCreateRequest(**create_book)
    mocker.patch.object(BookRepository, "create", return_value=book)

    service = get_book_service(mocker.MagicMock())

    with pytest.raises(ValueError) as exc_info:
        await service.create_book(book)
    assert str(exc_info.value) == expected_error_msg


@pytest.mark.parametrize(
    "book_presence, borrowed_books, expected_error_msg",
    ((False, 2, "Book doesn't exist."), (True, 3, "There are no available books.")),
)
async def test_borrow_creation_failure(
    mocker, create_book, create_user, book_presence, borrowed_books, expected_error_msg
):
    book_mock = None
    if book_presence:
        book_mock = mocker.MagicMock()
        book_mock.quantity = borrowed_books

    mocker.patch.object(BookRepository, "get_one", return_value=book_mock)
    mocker.patch.object(BorrowRepository, "get_borrowed_books", return_value=borrowed_books)

    borrow_create = BorrowCreateRequest(isbn="978-0-262-13472-9")
    user = UserCreateRequest(**create_user)

    service = get_borrow_service(mocker.MagicMock())

    with pytest.raises(ValueError) as exc_info:
        await service.borrow(borrow_create, user)
    assert str(exc_info.value) == expected_error_msg


async def test_return_book_success(mocker):
    mocker.patch.object(BorrowRepository, "get_one", return_value=True)
    mocker.patch.object(BorrowRepository, "return_book", return_value=None)

    service = get_borrow_service(mocker.MagicMock())

    borrow_create = BookReturnRequest(isbn="978-0-262-13472-9")
    user = mocker.MagicMock()
    user.id = 1
    borrow = await service.book_return(borrow_create, user)
    assert borrow is True


async def test_return_book_failure(mocker):
    mocker.patch.object(BorrowRepository, "get_one", return_value=None)
    service = get_borrow_service(mocker.MagicMock())

    borrow_create = BookReturnRequest(isbn="978-0-262-13472-9")
    user = mocker.MagicMock()
    user.id = 1

    with pytest.raises(ValueError) as exc_info:
        await service.book_return(borrow_create, user)
    assert str(exc_info.value) == "You can not return the book that you didn't take before."
