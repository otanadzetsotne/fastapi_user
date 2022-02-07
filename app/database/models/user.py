from sqlalchemy import Boolean, Column, Integer, String

from ..base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), nullable=False, unique=True, index=True)
    password_hash = Column(String(60), nullable=False)
    name = Column(String(60), nullable=True)
    surname = Column(String(60), nullable=True)
    phone = Column(String(15), nullable=True)
    disabled = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
