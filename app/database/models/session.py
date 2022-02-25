from sqlalchemy import ForeignKey, Column, Integer, String, DateTime

from ..base import Base


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    agent = Column(String(), nullable=False)
    token = Column(String(60), nullable=False)
    expires = Column(DateTime, nullable=False)
