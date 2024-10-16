from datetime import date

from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "authors"

    name: Mapped[str] = mapped_column(unique=True)
    surname: Mapped[str]
    birthdate: Mapped[date]

    books = relationship("Book", back_populates="author")
