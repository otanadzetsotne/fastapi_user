from typing import Optional

from pydantic import BaseModel, Field


class TokenOut(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)


class TokenData(BaseModel):
    username: Optional[str] = Field(...)
