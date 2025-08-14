from abc import ABC, abstractmethod
from typing import Any, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import and_, delete, exists, insert, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.exceptions.exceptions import DBNotFoundError

BaseModeGeneric = TypeVar("BaseModeGeneric", bound=BaseModel)


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, **kwargs: Any) -> int | UUID:
        """Add a single record to the repository.

        Args:
            kwargs: Arbitrary keyword arguments for the record to be added.

        Returns:
            The ID of the newly added record, which can be either an integer or UUID.
        """
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, *args: Any, **kwargs: Any) -> list[BaseModel]:
        """Find all records in the repository.

        Args:
            args: Arbitrary positional arguments.
            kwargs: Arbitrary keyword arguments.

        Returns:
            A list of all records represented as instances of BaseModel.
        """
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model: Any

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the repository with a database session.

        Args:
            session: An instance of AsyncSession to interact with the database.
        """
        self.session = session

    async def add_one(self, **kwargs: Any) -> int | UUID:
        stmt = insert(self.model).values(**kwargs).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def add_all(self, data: list[BaseModeGeneric]) -> None:
        """Add multiple records to the database.

        Args:
            data: A list of pydantic classes instances to be added to the database.
        """
        data_dict = [item.model_dump() for item in data]
        orm_objects = [self.model(**item) for item in data_dict]
        self.session.add_all(orm_objects)
        await self.session.flush()

    async def edit_one(self, row_id: int | UUID, data: dict) -> int | UUID:
        """Edit a single record in the database.

        Args:
            row_id: The ID of the record to be edited, which can be either an integer or UUID.
            data: A dictionary containing the data to update the record with.

        Returns:
            The ID of the edited record, which can be either an integer or UUID.

        Raises:
            DBNotFoundError: If no record with the given ID is found.
        """
        try:
            stmt = update(self.model).values(**data).filter_by(id=row_id).returning(self.model.id)
            res = await self.session.execute(stmt)
            res = res.scalar_one()
        except NoResultFound:
            raise DBNotFoundError(self.model.__tablename__, row_id)
        return res

    async def find_all(self) -> list[Any]:
        stmt = select(self.model)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_all_with_conditional(self, **filter_by: Any) -> list[Any]:
        """Find all records in the database based on specific conditions.

        Args:
            filter_by: Arbitrary keyword arguments to filter the records by.

        Returns:
            A list of records that match the conditions, represented as instances of BaseModel.

        Notes:
            Each of your sqlalchemy models must have an implementation of the to_read_model() function,
            which returns the pydantic model from the sqlalchemy model.
        """
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def find_one(self, **filter_by: Any) -> Any:
        """Find a single record in the database based on specific conditions.

        Args:
            filter_by: Arbitrary keyword arguments to filter the record by.

        Returns:
            The record that matches the conditions, represented as an instance of BaseModel.

        Raises:
            DBNotFoundError: If no record matching the conditions is found.
        """
        stmt = select(self.model).filter_by(**filter_by)
        try:
            res = await self.session.execute(stmt)
            res = res.scalar_one().to_read_model()
        except NoResultFound:
            raise DBNotFoundError(self.model.__tablename__, filter_by.get("id", "Some Id"))
        return res

    async def exist(self, **filter_by: Any) -> bool:
        """Check if any record exists in the database based on specific conditions.

        Args:
            filter_by: Arbitrary keyword arguments to filter the record by.

        Returns:
            A boolean value indicating whether a record that matches the conditions exists.
        """
        conditions = [getattr(self.model, key) == value for key, value in filter_by.items()]
        query = select(exists().where(and_(*conditions)))
        result = await self.session.execute(query)
        return result.scalar()

    async def delete_one(self, **kwargs: Any) -> None:
        """Delete a single record from the database based on specific conditions.

        Args:
            kwargs: Arbitrary keyword arguments to filter the record by.

        Raises:
            DBNotFoundError: If no record matching the conditions is found.
        """
        stmt = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(stmt)
        instance = result.scalars().first()
        if instance:
            await self.session.delete(instance)
        else:
            raise DBNotFoundError(self.model.__tablename__, kwargs.get("id", "Some Id"))

    async def delete_all(self, **kwargs: Any) -> None:
        """Delete multiple records from the database based on specific conditions.

        Args:
            kwargs: Arbitrary keyword arguments to filter the records by.
        """
        stmt = delete(self.model).filter_by(**kwargs)
        await self.session.execute(stmt)
