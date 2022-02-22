import databases
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from ..dependencies.settings import get_settings


settings = get_settings()


name = settings.db.name
host = settings.db.host
port = settings.db.port
user = settings.db.user
password = settings.db.password
subd = settings.db.subd
engine = settings.db.engine
database_url = f'{subd}+{engine}://{user}:{password}@{host}:{port}/{name}'


db = databases.Database(database_url)
Base = declarative_base()
metadata = MetaData()
