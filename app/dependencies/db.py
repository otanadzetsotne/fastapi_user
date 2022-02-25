from sqlalchemy.ext.asyncio import AsyncSession

from ..database.base import db_session


async def get_db_session():
    loc_db_session: AsyncSession = db_session()

    try:
        yield loc_db_session
    finally:
        await loc_db_session.commit()
        await loc_db_session.close()
