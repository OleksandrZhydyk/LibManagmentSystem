from datetime import date
from typing import TYPE_CHECKING

from database.base import Base
from database.models.many_to_many import book_author_association
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models import Book


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(unique=True)
    surname: Mapped[str]
    birthdate: Mapped[date]

    books: Mapped[list["Book"]] = relationship(secondary=book_author_association, back_populates="authors")
