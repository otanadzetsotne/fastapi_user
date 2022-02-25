from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from ..dependencies.settings import get_settings


# Get settings
settings = get_settings()

# Create DB url
name = settings.db.name
host = settings.db.host
port = settings.db.port
user = settings.db.user
password = settings.db.password
subd = settings.db.subd
engine = settings.db.engine
database_url = f'{subd}+{engine}://{user}:{password}@{host}:{port}/{name}'

# Set up ORM
Base = declarative_base()
db_engine = create_async_engine(database_url)
db_session = sessionmaker(
    bind=db_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
