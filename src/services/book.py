from dto.repository import SearchFieldDTO
from filters import BookFilter
from repositories.author import AuthorRepository
from repositories.book import BookRepository
from repositories.genre import GenreRepository
from repositories.publisher import PublisherRepository
from schemas.book import BookCreateRequest


class BookService:
    """
    BookService provides business logic for handling books.

    Attributes:
        book_repo (BookRepository): The repository for book-related
            database operations.
    """

    def __init__(
        self,
        book_repo: BookRepository,
        author_repo: AuthorRepository,
        publisher_repo: PublisherRepository,
        genre_repo: GenreRepository,
    ):
        """
        Initialize the BookService with a BookRepository instance.

        Args:
            book_repo (BookRepository): The repository for handling,
                book data.
        """
        self.book_repo = book_repo
        self.author_repo = author_repo
        self.publisher_repo = publisher_repo
        self.genre_repo = genre_repo

    async def create_book(self, book: BookCreateRequest):
        isbn_unique = [SearchFieldDTO(column="isbn", value=book.isbn)]

        if await self.book_repo.exists(search_fields=isbn_unique):
            raise ValueError(f"Book ISBN {book.isbn} already exists.")

        authors = await self.author_repo.get_authors(book.authors)

        if authors.missing_authors:
            raise ValueError("Author doesn't exist.")

        genre = await self.genre_repo.get_one([SearchFieldDTO(column="name", value=book.genre)])
        if not genre:
            raise ValueError("Genre doesn't exist.")

        publisher = await self.publisher_repo.get_one([SearchFieldDTO(column="name", value=book.publisher)])
        if not publisher:
            raise ValueError("Publisher doesn't exist.")

        book_dct = book.model_dump()
        book_dct["authors"] = authors.found_authors
        book_dct["genre"] = genre
        book_dct["publisher"] = publisher

        return await self.book_repo.create(**book_dct)

    async def get_all(self, user_ordering: BookFilter):
        return await self.book_repo.get_all(user_ordering)

    async def get_book_history(self, pk: int):
        return await self.book_repo.get_book_history(pk)
