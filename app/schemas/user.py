from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserData(UserBase):
    password_hash: str
    disabled: bool = False
    confirmed: bool = False

    class Config:
        orm_mode = True


class User(UserData):
    id: int
