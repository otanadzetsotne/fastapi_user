from sqlalchemy import func
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(320), nullable=False, unique=True, index=True)
    password_hash = Column(String(60), nullable=False)
    name = Column(String(60), nullable=True)
    surname = Column(String(60), nullable=True)
    phone = Column(String(25), nullable=True)
    disabled = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)
    created = Column(DateTime, server_default=func.now())

    sessions = relationship('Session', back_populates='user')
    client = relationship('Client', back_populates='user', uselist=False)
