from database.models import Book
from fastapi_pagination.ext.sqlalchemy import paginate
from repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class BookRepository(BaseRepository):
    model = Book

    async def get_all(self, user_ordering):
        query = select(self.model)
        sorted_query = user_ordering.sort(query)
        return await paginate(self.session, sorted_query)

    async def get_book_history(self, pk: int):
        query = select(self.model).where(self.model.id == pk).options(joinedload(self.model.borrow_history))
        db_obj = await self.session.execute(query)
        return db_obj.scalar().borrow_history
