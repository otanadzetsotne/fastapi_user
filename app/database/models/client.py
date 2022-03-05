from sqlalchemy import func
from sqlalchemy import ForeignKey, Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from ..base import Base


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    secret = Column(String, nullable=False)
    expires = Column(DateTime, nullable=False)

    user = relationship('User', back_populates='client')
