from datetime import date

from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    birthdate: Mapped[date]

    borrowed_book = relationship("Book", back_populates="borrower")
