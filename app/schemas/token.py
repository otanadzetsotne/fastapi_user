from typing import Optional

from pydantic import BaseModel, Field, EmailStr

from .user import User
from .session import Session


class TokenOut(BaseModel):
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    token_type: str = Field(...)


class TokenData(BaseModel):
    user_id: int = Field(...)
    username: EmailStr = Field(...)


class AccessTokenChecked(BaseModel):
    token: str = Field(...)
    payload: dict = Field(...)
    user: Optional[User] = Field(None)


class RefreshTokenChecked(AccessTokenChecked):
    session: Session = Field(...)
