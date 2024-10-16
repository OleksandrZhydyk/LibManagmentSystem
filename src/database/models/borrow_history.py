import datetime

from database.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class BorrowHistory(Base):
    __tablename__ = "borrows"

    borrower_name: Mapped[str]
    borrower_surname: Mapped[str]
    borrow_date: Mapped[datetime.date] = mapped_column(default=datetime.datetime.now(datetime.UTC))
    return_date: Mapped[datetime.date]
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="SET NULL"))
    borrower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    book_name: Mapped[str]

    book = relationship("Book", back_populates="borrow_history")
    borrower = relationship("User", back_populates="borrowed_book")
