from datetime import datetime

from pydantic import BaseModel, Field, IPvAnyAddress


class Agent(BaseModel):
    host: IPvAnyAddress
    user_agent: str

    def __str__(self):
        return f'{self.host} {self.user_agent}'


class SessionAgent(BaseModel):
    user_id: int = Field(...)
    agent: str = Field(...)


class SessionData(SessionAgent):
    token: str = Field(..., max_length=60)
    expires: datetime = Field(...)


class Session(SessionData):
    id: int = Field(...)
