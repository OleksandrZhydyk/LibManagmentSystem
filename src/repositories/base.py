from collections.abc import Sequence
from typing import Any

from database.base import Base
from dto.repository import SearchFieldDTO
from sqlalchemy import and_, delete, exists, select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    BaseRepository provides common CRUD operations for SQLAlchemy models,
        with asynchronous support.

    Attributes:
        model (Any): The SQLAlchemy model associated with the repository.
        session (AsyncSession): The asynchronous database session, used for
            operations.
    """

    model: Base = None

    def __init__(self, session: AsyncSession):
        """
        Initializes the BaseRepository instance with a database session.

        Args:
            session (AsyncSession): The asynchronous database session,
                used for operations.
        """
        self.session = session

    async def get_all(self, *args, **kwargs) -> Sequence:
        """
        Fetch all instances of the associated model from the database.

        Returns:
            List: A list of instances of the associated model.
        """
        query = select(self.model)
        response = await self.session.execute(query)
        return response.scalars().all()

    async def create(self, **kwargs) -> Any:
        """
        Create a new instance of the model with the provided keyword arguments.

        Args:
            **kwargs: Keyword arguments representing the fields of the model.

        Returns:
            Any: The created instance of the model.
        """
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        return instance

    async def exists(self, search_fields: list[SearchFieldDTO]) -> bool:
        filters = self._construct_filters(search_fields)
        query = select(exists().where(and_(*filters)))
        res = await self.session.execute(query)
        return res.scalar()

    async def get_one(self, search_fields: list[SearchFieldDTO]) -> Any:
        """
        Fetch a single instance from the database based on the provided query.

        Args:
            search_fields (SearchFieldDTO): DTO that keeps column name and value for filtering.

        Returns:
            Any: The fetched instance or None if not found.
        """
        filters = self._construct_filters(search_fields)
        query = select(self.model).where(and_(*filters))
        response = await self.session.execute(query)
        return response.scalars().first()

    async def delete(self, pk: int) -> None:
        """
        Deletes an instance from the database using its ID.

        Args:
            pk (int): The ID of the instance to be deleted.
        """
        query = delete(self.model).where(self.model.id == pk)
        await self.session.execute(query)
        await self.session.commit()

    async def save(self, obj: Any) -> None:
        """
        Adds and commits an instance to the database session.

        Args:
            obj (Any): The instance to be saved.
        """
        self.session.add(obj)
        await self.session.commit()

    def _construct_filters(self, search_fields: list[SearchFieldDTO]) -> list:
        filters = []
        for field in search_fields:
            column = getattr(self.model, field.column)
            expression = getattr(column, field.operator)(field.value)
            filters.append(expression)
        return filters
