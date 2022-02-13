from databases import Database

from .base import CRUD
from ..database.models import sessions
from ..schemas.session import SessionData, SessionAgent, Session


class CRUDSession(CRUD):
    model = sessions
    schema = Session
    schema_create = SessionData
    schema_update = SessionData

    @classmethod
    async def delete(
            cls,
            db: Database,
            session: SessionAgent,
    ):
        return await cls.delete_where(
            db,
            cls.model.c.user_id == session.user_id,
            cls.model.c.agent == session.agent,
        )

    @classmethod
    async def update(
            cls,
            db: Database,
            session: SessionData,
    ):
        return await cls.update_where(
            db,
            cls.model.c.user_id == session.user_id,
            cls.model.c.agent == session.agent,
            refresh_token=session.token,
            expires=session.expires,
        )
