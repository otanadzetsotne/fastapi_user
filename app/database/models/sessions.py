from sqlalchemy import Table, ForeignKey, Column, Integer, String, DateTime

from ..base import metadata


sessions = Table(
    'sessions',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('agent', String(), nullable=False),
    Column('token', String(60), nullable=False),
    Column('expires', DateTime(), nullable=False),
)
