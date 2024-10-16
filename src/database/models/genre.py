from database.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Genre(Base):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(unique=True)
