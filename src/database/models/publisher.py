from datetime import date

from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Publisher(Base):
    __tablename__ = "publishers"

    name: Mapped[str] = mapped_column(unique=True)
    established_year: Mapped[date]
