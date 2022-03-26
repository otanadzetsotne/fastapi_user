from enum import Enum
from datetime import timedelta

from pydantic import BaseModel, BaseSettings


class Environment(Enum):
    prod = 'prod'
    test = 'test'
    dev = 'dev'


class Secret(BaseModel):
    jwt_key: str
    refresh_key: str
    confirm_key: str
    client_key: str


class Token(BaseModel):
    type: str = 'bearer'
    algorithm: str = 'HS256'
    client_length: int = 255
    client_entropy: int = 56

    access_iss = 'auth'
    confirm_iss = 'confirm'
    password_reset_iss = 'password_reset'
    client_iss = 'client'

    access_expires: timedelta = timedelta(hours=1)
    refresh_expires: timedelta = timedelta(days=30)
    confirm_expires: timedelta = timedelta(days=30)
    client_expires: timedelta = timedelta(hours=1)
    client_secret_expires: timedelta = timedelta(days=365)


class SMTP(BaseModel):
    msg_from: str
    host: str
    port: int


class DataBase(BaseModel):
    name: str
    name_testing: str
    host: str
    port: str
    user: str
    password: str
    subd: str
    engine: str


class Sentry(BaseModel):
    url: str
    traces_sample_rate: float = 1.0


class Settings(BaseSettings):
    smtp: SMTP
    db: DataBase
    secret: Secret
    sentry: Sentry
    token: Token = Token()
    environment: Environment = Environment.prod

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
