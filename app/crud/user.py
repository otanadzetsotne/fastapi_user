from ..database import models
from ..database.base import db
from ..schemas import UserData, User


async def get(user_id: int):
    query = models.users.select().where(models.users.id == user_id)
    user = await db.fetch_one(query)

    return user


async def get_by_email(email: str):
    query = models.users.select().where(models.users.columns.email == email)
    user = await db.fetch_one(query)

    return user


async def get_multi(skip: int = 0, limit: int = 100):
    query = models.users.select().offset(skip).limit(limit)
    users = await db.fetch_all(query)

    return users


async def create(user: UserData) -> User:
    query = models.users.insert().values(**user.dict())
    user_id = await db.execute(query)
    user_db = User(id=user_id, **user.dict())

    return user_db
