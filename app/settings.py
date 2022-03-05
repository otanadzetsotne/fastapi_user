from datetime import timedelta

from pydantic import BaseModel, BaseSettings


class Secret(BaseModel):
    jwt_key: str
    refresh_key: str
    confirm_key: str
    client_key: str


# class _SettingsDB(BaseModel):
#     url: str


class Token(BaseModel):
    type: str = 'bearer'
    algorithm: str = 'HS256'
    client_length: int = 1024
    client_entropy: int = 56
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
    host: str
    port: str
    user: str
    password: str
    subd: str
    engine: str


class Settings(BaseSettings):
    db: DataBase
    smtp: SMTP
    secret: Secret
    token: Token = Token()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
