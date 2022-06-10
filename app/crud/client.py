from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUD
from database.models import Client as ClientModel
from schemas import ClientMeta, ClientData, Client


class CRUDClient(CRUD):
    model = ClientModel
    schema = Client
    schema_create = ClientData
    schema_update = ClientData

    @classmethod
    async def get_by_user_id(
            cls,
            db: AsyncSession,
            user_id: int,
    ):
        return await cls.get_first(db, cls.model.user_id == user_id)

    @classmethod
    async def get_by_client_meta(
            cls,
            db: AsyncSession,
            client_meta: ClientMeta,
    ):
        return await cls.get_first(
            db,
            cls.model.user_id == client_meta.user_id,
            cls.model.secret == client_meta.secret,
        )

    @classmethod
    async def delete_by_user_id(
            cls,
            db: AsyncSession,
            user_id: int,
    ):
        return await cls.delete_where(db, cls.model.user_id == user_id)
