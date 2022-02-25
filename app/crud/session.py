from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUD
from ..database.models import Session as SessionModel
from ..schemas import SessionData, SessionAgent, Session, SessionMeta


class CRUDSession(CRUD):
    model = SessionModel
    schema = Session
    schema_create = SessionData
    schema_update = SessionData

    @classmethod
    async def delete_by_agent(
            cls,
            db: AsyncSession,
            session: SessionAgent,
    ):
        return await cls.delete_first(
            db,
            cls.model.user_id == session.user_id,
            cls.model.agent == session.agent,
        )

    @classmethod
    async def update_by_agent(
            cls,
            db: AsyncSession,
            session: SessionData,
    ) -> Session:
        return await cls.update_first(
            db,
            cls.model.user_id == session.user_id,
            cls.model.agent == session.agent,
            refresh_token=session.token,
            expires=session.expires,
        )

    @classmethod
    async def get_by_meta(
            cls,
            db: AsyncSession,
            session: SessionMeta,
    ) -> Session:
        return await cls.get_first(
            db,
            cls.model.user_id == session.user_id,
            cls.model.agent == session.agent,
            cls.model.token == session.token,
        )
