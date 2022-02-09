from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    name: Optional[str] = Field(None)
    surname: Optional[str] = Field(None)
    phone: Optional[str] = Field(None)

    # TODO: phone number validation


class UserIn(UserBase):
    password: str = Field(...)


class UserData(UserBase):
    password_hash: str = Field(...)
    disabled: bool = Field(False)
    confirmed: bool = Field(False)

    class Config:
        orm_mode = True


class User(UserData):
    id: int = Field(...)
