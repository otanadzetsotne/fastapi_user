from databases import Database

from .base import CRUD
from ..database.models import sessions
from ..schemas.session import SessionData, SessionAgent, Session, SessionMeta


class CRUDSession(CRUD):
    model = sessions
    schema = Session
    schema_create = SessionData
    schema_update = SessionData

    @classmethod
    async def delete_by_agent(
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
    async def update_by_agent(
            cls,
            db: Database,
            session: SessionData,
    ) -> Session:
        return await cls.update_where(
            db,
            cls.model.c.user_id == session.user_id,
            cls.model.c.agent == session.agent,
            refresh_token=session.token,
            expires=session.expires,
        )

    @classmethod
    async def get_by_meta(
            cls,
            db: Database,
            session: SessionMeta,
    ) -> Session:
        return await cls.get_where(
            db,
            cls.model.c.user_id == session.user_id,
            cls.model.c.agent == session.agent,
            cls.model.c.token == session.token,
        )
