from dto.repository import SearchFieldDTO
from repositories.publisher import PublisherRepository
from schemas.publisher import PublisherCreateRequest


class PublisherService:
    """
    PublisherService provides business logic for handling publishers.

    Attributes:
        publisher_repo (PublisherRepository): The repository for publisher-related
            database operations.
    """

    def __init__(self, publisher_repo: PublisherRepository):
        """
        Initialize the PublisherService with a PublisherRepository instance.

        Args:
            publisher_repo (PublisherRepository): The repository for handling,
                Publisher data.
        """
        self.publisher_repo = publisher_repo

    async def create_publisher(self, publisher: PublisherCreateRequest):
        fields = [SearchFieldDTO(column="name", value=publisher.name)]
        if await self.publisher_repo.exists(search_fields=fields):
            raise ValueError(f"Publisher {publisher.name} already exists.")
        return await self.publisher_repo.create(**publisher.model_dump())

    async def get_all(self):
        return await self.publisher_repo.get_all()
