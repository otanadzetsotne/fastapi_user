from pydantic import EmailStr
from databases import Database

from ..database.models import users
from ..schemas import UserData, User
from .base import CRUD


class CRUDUser(CRUD):
    model = users
    schema = User
    schema_create = UserData
    schema_update = UserData

    @classmethod
    async def get_by_email(
            cls,
            db: Database,
            email: EmailStr,
    ):
        return await cls.get_where(db, cls.model.c.email == email)

    @classmethod
    async def get_by_username(
            cls,
            db: Database,
            username: str,
    ):
        return await cls.get_where(db, cls.model.c.username == username)
