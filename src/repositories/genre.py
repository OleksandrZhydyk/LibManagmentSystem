from database.models import Genre
from repositories.base import BaseRepository


class GenreRepository(BaseRepository):
    model = Genre
