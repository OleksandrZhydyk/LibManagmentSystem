from database.models import Author
from dto.repository import AuthorsExistDTO
from repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class AuthorRepository(BaseRepository):
    model = Author

    async def get_authors(self, author_names: list[str]) -> AuthorsExistDTO:
        query = select(self.model).where(self.model.name.in_(author_names))
        db_authors = await self.session.execute(query)
        db_authors = db_authors.scalars().all()

        found_authors = [author.name for author in db_authors]
        missing_authors = set(author_names) - set(found_authors)

        return AuthorsExistDTO(found_authors=db_authors, missing_authors=list(missing_authors))

    async def get_author_books(self, pk: int):
        query = select(self.model).where(self.model.id == pk).options(joinedload(self.model.books))
        db_obj = await self.session.execute(query)
        return db_obj.scalar().books
