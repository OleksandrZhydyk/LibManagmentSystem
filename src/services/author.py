from dto.repository import SearchFieldDTO
from repositories.author import AuthorRepository
from schemas.author import AuthorCreateRequest


class AuthorService:
    """
    AuthorService provides business logic for handling authors.

    Attributes:
        author_repo (AuthorsRepository): The repository for author-related
            database operations.
    """

    def __init__(self, author_repo: AuthorRepository):
        """
        Initialize the AuthorService with a AuthorRepository instance.

        Args:
            author_repo (AuthorRepository): The repository for handling,
                Author data.
        """
        self.author_repo = author_repo

    async def create_author(self, author: AuthorCreateRequest):
        fields = [SearchFieldDTO(column="name", value=author.name)]
        if await self.author_repo.exists(search_fields=fields):
            raise ValueError(f"Author {author.name} already exists.")
        return await self.author_repo.create(**author.model_dump())

    async def get_author_books(self, pk: int):
        fields = [SearchFieldDTO(column="id", value=pk)]
        if not await self.author_repo.exists(search_fields=fields):
            raise ValueError("Author doesn't exist.")
        return await self.author_repo.get_author_books(pk)

    async def get_all(self):
        return await self.author_repo.get_all()
