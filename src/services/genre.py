from dto.repository import SearchFieldDTO
from repositories.genre import GenreRepository
from schemas.genre import GenreCreateRequest


class GenreService:
    """
    PublisherService provides business logic for handling genres.

    Attributes:
        genre_repo (GenreRepository): The repository for genre-related
            database operations.
    """

    def __init__(self, genre_repo: GenreRepository):
        """
        Initialize the GenreService with a GenreRepository instance.

        Args:
            genre_repo (GenreRepository): The repository for handling,
                Genre data.
        """
        self.genre_repo = genre_repo

    async def create_genre(self, genre: GenreCreateRequest):
        fields = [SearchFieldDTO(column="name", value=genre.name)]
        if await self.genre_repo.exists(search_fields=fields):
            raise ValueError(f"Genre {genre.name} already exists.")
        return await self.genre_repo.create(**genre.model_dump())

    async def get_all(self):
        return await self.genre_repo.get_all()
