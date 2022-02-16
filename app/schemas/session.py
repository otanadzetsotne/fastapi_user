from datetime import datetime

from pydantic import BaseModel, Field


class SessionAgent(BaseModel):
    user_id: int = Field(...)
    agent: str = Field(...)


class SessionMeta(SessionAgent):
    token: str = Field(..., max_length=60)


class SessionData(SessionMeta):
    expires: datetime = Field(...)


class Session(SessionData):
    id: int = Field(...)
