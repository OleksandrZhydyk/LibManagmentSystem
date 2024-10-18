from database.models import BorrowHistory, User
from dto.repository import SearchFieldDTO
from repositories.book import BookRepository
from repositories.borrows import BorrowRepository
from repositories.user import UserRepository
from schemas.borrows import BookReturnRequest, BorrowCreateRequest


class BorrowService:
    def __init__(self, borrow_repo: BorrowRepository, book_repo: BookRepository, user_repo: UserRepository) -> None:
        self.borrow_repo = borrow_repo
        self.book_repo = book_repo
        self.user_repo = user_repo

    async def borrow(self, borrow_create: BorrowCreateRequest, user: User) -> BorrowHistory:
        book = await self.book_repo.get_one([SearchFieldDTO(column="isbn", value=borrow_create.isbn)])
        borrowed_books: int = await self.borrow_repo.get_borrowed_books(book)

        if borrowed_books >= book.quantity:
            raise ValueError("There are no available books.")

        borrow_dct = {
            "borrower": user,
            "borrower_name": user.name,
            "borrower_surname": user.surname,
            "book": book,
            "book_name": book.title,
            "book_isbn": book.isbn,
        }
        return await self.borrow_repo.create(**borrow_dct)

    async def book_return(self, book_return: BookReturnRequest, user: User) -> BorrowHistory:
        borrow = await self.borrow_repo.get_one(
            [
                SearchFieldDTO(column="borrower_id", value=user.id),
                SearchFieldDTO(column="book_isbn", value=book_return.isbn),
                SearchFieldDTO(column="return_date", value=None),
            ]
        )

        await self.borrow_repo.return_book(borrow)
        return borrow
