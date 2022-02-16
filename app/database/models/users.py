from sqlalchemy import Table, Boolean, Column, Integer, String
from ..base import metadata


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('username', String(320), nullable=False, unique=True, index=True),
    Column('password_hash', String(60), nullable=False),
    Column('name', String(60), nullable=True),
    Column('surname', String(60), nullable=True),
    Column('phone', String(15), nullable=True),
    Column('disabled', Boolean, default=False),
    Column('confirmed', Boolean, default=False),
)
