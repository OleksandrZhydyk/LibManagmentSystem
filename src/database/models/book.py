from datetime import date
from typing import TYPE_CHECKING

from database.base import Base
from database.models import Author
from database.models.many_to_many import book_author_association
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models import Author


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    description: Mapped[str]
    isbn: Mapped[str] = mapped_column(unique=True, nullable=False)
    publish_date: Mapped[date] = mapped_column(nullable=False)
    quantity: Mapped[int]

    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))

    authors: Mapped[list["Author"]] = relationship(secondary=book_author_association, back_populates="books")

    genre = relationship("Genre")
    publisher = relationship("Publisher")
    borrow_history = relationship("BorrowHistory", back_populates="book")
