from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUD
from ..database.models import User as UserModel
from ..schemas import UserData, User


class CRUDUser(CRUD):
    model = UserModel
    schema = User
    schema_create = UserData
    schema_update = UserData

    @classmethod
    async def get_by_username(
            cls,
            db: AsyncSession,
            username: str,
    ) -> User:
        return await cls.first(db, cls.model.username == username)
