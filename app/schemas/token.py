from typing import Optional

from pydantic import BaseModel, Field


class TokenOut(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(...)


class TokenData(BaseModel):
    # TODO: Add more data
    username: Optional[str] = Field(...)
