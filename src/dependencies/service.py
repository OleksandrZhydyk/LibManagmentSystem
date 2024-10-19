from database.base import get_session
from fastapi import Depends
from repositories.author import AuthorRepository
from repositories.book import BookRepository
from repositories.borrows import BorrowRepository
from repositories.genre import GenreRepository
from repositories.publisher import PublisherRepository
from repositories.user import UserRepository
from services.auth import AuthService
from services.author import AuthorService
from services.book import BookService
from services.borrows import BorrowService
from services.genre import GenreService
from services.publisher import PublisherService
from sqlalchemy.ext.asyncio import AsyncSession


def get_genre_service(
    session: AsyncSession = Depends(get_session),
) -> GenreService:
    """
    Dependency function to obtain a GenreService instance with a given
        AsyncSession.

    Args:
        session (AsyncSession, optional): An optional AsyncSession dependency
            obtained from get_session. Defaults to Depends(get_session).

    Returns:
        GenreService: An instance of the GenreService with the provided
            AsyncSession.
    """
    repo = GenreRepository(session)
    return GenreService(genre_repo=repo)


def get_publisher_service(session: AsyncSession = Depends(get_session)) -> PublisherService:
    repo = PublisherRepository(session)
    return PublisherService(publisher_repo=repo)


def get_author_service(session: AsyncSession = Depends(get_session)) -> AuthorService:
    repo = AuthorRepository(session)
    return AuthorService(author_repo=repo)


def get_book_service(session: AsyncSession = Depends(get_session)) -> BookService:
    book_repo = BookRepository(session)
    author_repo = AuthorRepository(session)
    publisher_repo = PublisherRepository(session)
    genre_repo = GenreRepository(session)
    return BookService(
        book_repo=book_repo, author_repo=author_repo, publisher_repo=publisher_repo, genre_repo=genre_repo
    )


def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    repo = UserRepository(session)
    return AuthService(user_repo=repo)


def get_borrow_service(session: AsyncSession = Depends(get_session)) -> BorrowService:
    borrow_repo = BorrowRepository(session)
    book_repo = BookRepository(session)
    return BorrowService(borrow_repo=borrow_repo, book_repo=book_repo)
