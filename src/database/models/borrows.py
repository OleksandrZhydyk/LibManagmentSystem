import datetime
from typing import TYPE_CHECKING

from database.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models import Book, User


class BorrowHistory(Base):
    __tablename__ = "borrow_history"

    borrower_name: Mapped[str]
    borrower_surname: Mapped[str]
    borrow_date: Mapped[datetime.date] = mapped_column(TIMESTAMP(timezone=True), default=datetime.date.today)
    return_date: Mapped[datetime.date | None] = mapped_column(TIMESTAMP(timezone=True), default=None)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="SET NULL"))
    borrower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    book_name: Mapped[str]
    book_isbn: Mapped[str]

    book: Mapped["Book"] = relationship("Book", back_populates="borrow_history")
    borrower: Mapped["User"] = relationship("User", back_populates="borrowed_book")
