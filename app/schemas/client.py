from datetime import datetime

from pydantic import BaseModel, Field


class ClientSecret(BaseModel):
    secret: str = Field(...)


class ClientMeta(ClientSecret):
    user_id: int = Field(...)


class ClientData(ClientMeta):
    expires: datetime = Field(...)


class Client(ClientData):
    id: int = Field(...)
