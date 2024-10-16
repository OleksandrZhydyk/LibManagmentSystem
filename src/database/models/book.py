from datetime import date

from database.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Book(Base):
    __tablename__ = "books"

    title: Mapped[str]
    description: Mapped[str]
    isbn: Mapped[str] = mapped_column(unique=True, nullable=False)
    publish_date: Mapped[date] = mapped_column(nullable=False)
    quantity: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publishers.id"))

    author = relationship("Author", back_populates="books")
    genre = relationship("Genre")
    publisher = relationship("Publisher")
    borrow_history = relationship("Borrow", back_populates="book")
