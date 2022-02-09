from datetime import timedelta

from pydantic import BaseModel, BaseSettings


class Secret(BaseModel):
    jwt_key: str  # SECRET_KEY


# class _SettingsDB(BaseModel):
#     url: str


class Token(BaseModel):
    type: str = 'bearer'  # ACCESS_TOKEN_ALGORITHM
    algorithm: str = 'HS256'  # ACCESS_TOKEN_EXPIRES
    expires: timedelta = timedelta(minutes=30)  # ACCESS_TOKEN_TYPE


class Settings(BaseSettings):
    # db: _SettingsDB
    secret: Secret
    token: Token = Token()

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_nested_delimiter = '__'
