from abc import ABCMeta
from typing import Type, TypeVar, Optional

from pydantic import BaseModel
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import select, delete, update, insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.base import Base


TableType = TypeVar('TableType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUD(metaclass=ABCMeta):
    model: Type[TableType]
    schema: Type[SchemaType]
    schema_create: Type[CreateSchemaType]
    schema_update: Type[UpdateSchemaType]

    @staticmethod
    def query_where(
            query,
            *statements: list[BinaryExpression],
    ):
        if statements:
            query = query.where(*statements)

        return query

    @staticmethod
    def query_offset_limit(
            query,
            offset: int,
            limit: int,
    ):
        if offset:
            query = query.offset(offset)

        if limit:
            query = query.limit(limit)

        return query

    @classmethod
    def query_make(
            cls,
            query,
            *statements: list[BinaryExpression],
            offset: int,
            limit: int,
    ):
        query = cls.query_where(query, *statements)
        query = cls.query_offset_limit(query, offset=offset, limit=limit)

        return query

    @classmethod
    def query_select(
            cls,
            *statements: list[BinaryExpression],
            offset: int,
            limit: int,
    ):
        query = select(cls.model)
        query = cls.query_make(query, *statements, offset=offset, limit=limit)

        return query

    # Base executes

    @staticmethod
    async def execute(
            db: AsyncSession,
            query,
    ):
        return await db.execute(query)

    @classmethod
    async def execute_first(
            cls,
            db: AsyncSession,
            query,
    ):
        """
        Execute query and get first
        """

        result = await cls.execute(db, query)
        result = result.scalars().first()

        return result

    @classmethod
    async def execute_all(
            cls,
            db: AsyncSession,
            query,
    ):
        """
        Execute query and get all
        """

        result = await cls.execute(db, query)
        result = result.scalars().all()

        return result

    # Executes

    @classmethod
    async def create(
            cls,
            db: AsyncSession,
            entity: CreateSchemaType,
    ) -> SchemaType:
        """
        Create and select first
        """

        query = insert(cls.model).values(**dict(entity))

        result = await db.execute(query)
        entity_id = result.lastrowid

        return cls.schema(
            id=entity_id,
            **entity.dict(),
        )

    @classmethod
    async def delete_where(
            cls,
            db: AsyncSession,
            *statements,
    ):
        """
        Delete first
        """

        query = delete(cls.model)
        query = cls.query_where(query, *statements)

        await db.execute(query)

    @classmethod
    async def delete_by_id(
            cls,
            db: AsyncSession,
            entity_id: int,
    ):
        return await cls.delete_where(db, cls.model.id == entity_id)

    @classmethod
    async def update_first(
            cls,
            db: AsyncSession,
            *statements,
            **values,
    ):
        """
        Update and select first
        """

        query = update(cls.model)
        query = cls.query_where(query, *statements)
        query = query.values(**values)
        await cls.execute(db, query)

    @classmethod
    async def update_by_id(
            cls,
            db: AsyncSession,
            entity_id: int,
            **values,
    ):
        await cls.update_first(db, cls.model.id == entity_id, **values)

    @classmethod
    async def get_first(
            cls,
            db: AsyncSession,
            *statements: list[BinaryExpression],
    ) -> Optional[SchemaType]:
        """
        Select first element
        """

        query = cls.query_select(*statements, offset=0, limit=1)
        result = await cls.execute_first(db, query)
        if result:
            result = cls.schema(**result.__dict__)

        return result

    @classmethod
    async def get_id(
            cls,
            db: AsyncSession,
            *statements: list[BinaryExpression],
    ):
        query = cls.query_select(*statements, offset=0, limit=1)
        query = query.with_entities(cls.model.id)
        result = await cls.execute_first(db, query)

        return result

    @classmethod
    async def get_multi(
            cls,
            db: AsyncSession,
            *statements: list[BinaryExpression],
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ):
        query = cls.query_select(*statements, offset=offset, limit=limit)

        results = await db.execute(query)
        results = results.scalars().all()
        if results:
            results = [cls.schema(**result.__dict__) for result in results]

        return results

    @classmethod
    async def get_by_id(
            cls,
            db: AsyncSession,
            entity_id: int,
    ):
        return await cls.get_first(db, cls.model.id == entity_id)
