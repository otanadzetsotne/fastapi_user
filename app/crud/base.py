from typing import Type, TypeVar

from databases import Database
from pydantic import BaseModel
from sqlalchemy import Table
from sqlalchemy.sql.elements import BinaryExpression


TableType = TypeVar('TableType', bound=Table)
SchemaType = TypeVar('SchemaType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUD:
    model: Type[TableType]
    schema: Type[SchemaType]
    schema_create: Type[CreateSchemaType]
    schema_update: Type[UpdateSchemaType]

    @classmethod
    async def get_where(
            cls,
            db: Database,
            statement: BinaryExpression,
    ):
        query = cls.model.select().where(statement)
        result = await db.fetch_one(query)

        return result

    @classmethod
    async def get_multi(
            cls,
            db: Database,
            offset: int = 0,
            limit: int = 100,
    ):
        query = cls.model.select().offset(offset).limit(limit)
        entities = await db.fetch_all(query)

        return entities

    @classmethod
    async def create(
            cls,
            db: Database,
            entity: CreateSchemaType,
    ) -> SchemaType:
        query = cls.model.insert().values(**entity.dict())
        entity_id = await db.execute(query)
        entity_db = cls.schema(id=entity_id, **entity.dict())

        return entity_db

    @classmethod
    async def get(
            cls,
            db: Database,
            entity_id: int,
    ):
        return await cls.get_where(db, cls.model.columns.id == entity_id)
