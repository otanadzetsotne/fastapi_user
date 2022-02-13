import databases
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# DATABASE_URL = f'mysql+pymysql://mysql:@localhost/imsim'
DATABASE_URL = f'mysql+aiomysql://mysql:@localhost/imsim'
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

db = databases.Database(DATABASE_URL)
Base = declarative_base()
metadata = MetaData()
