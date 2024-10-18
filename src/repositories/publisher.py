from database.models import Publisher
from repositories.base import BaseRepository


class PublisherRepository(BaseRepository):
    model = Publisher
