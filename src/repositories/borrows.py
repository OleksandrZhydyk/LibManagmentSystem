import datetime

from database.models import BorrowHistory
from fastapi_pagination.ext.sqlalchemy import paginate
from repositories.base import BaseRepository
from sqlalchemy import and_, func, select


class BorrowRepository(BaseRepository):
    model = BorrowHistory

    async def get_all(self, book_ordering):
        query = select(self.model)
        sorted_query = book_ordering.sort(query)
        return await paginate(self.session, sorted_query)

    async def get_borrowed_books(self, book) -> int:
        query = select(func.count()).where(and_(self.model.book_id == book.id, self.model.return_date.is_(None)))
        result = await self.session.execute(query)
        return result.scalar()

    async def return_book(self, borrow: BorrowHistory):
        borrow.return_date = datetime.date.today()
        self.session.add(borrow)
        await self.session.commit()
