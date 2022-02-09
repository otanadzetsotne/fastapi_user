from ..database import models
from ..database.base import db
from ..schemas import UserData, User


async def create(user: UserData) -> User:
    query = models.users.insert().values(**user.dict())
    user_id = await db.execute(query)
    user_db = User(id=user_id, **user.dict())

    return user_db


async def get_multi(skip: int = 0, limit: int = 100):
    query = models.users.select().offset(skip).limit(limit)
    users = await db.fetch_all(query)

    return users


async def get_where(statement):
    query = models.users.select().where(statement)
    user = await db.fetch_one(query)

    return user


async def get(user_id: int):
    return await get_where(models.users.id == user_id)


async def get_by_username(username: str):
    return await get_where(models.users.columns.username == username)


async def get_by_email(email: str):
    return await get_where(models.users.columns.email == email)
