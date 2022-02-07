from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    disabled: bool
    confirmed: bool

    class Config:
        orm_mode = True
