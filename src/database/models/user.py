from datetime import date
from typing import TYPE_CHECKING

from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from database.models import BorrowHistory


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    birthdate: Mapped[date | None]
    is_active: Mapped[bool] = mapped_column(default=False)
    password: Mapped[str]

    borrowed_book: Mapped[list["BorrowHistory"]] = relationship("BorrowHistory", back_populates="borrower")
