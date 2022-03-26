from typing import TypeVar, Union

from pydantic import BaseModel, Field, EmailStr

from .session import Session
from ..dependencies.settings import get_settings, Settings


settings: Settings = get_settings()


class AccessTokenOut(BaseModel):
    access_token: str = Field(...)
    token_type: str = Field(...)
    expires_in: float = Field(...)


class AuthTokenOut(AccessTokenOut):
    refresh_token: str = Field(...)


class ClientTokenOut(AccessTokenOut):
    pass


# Payloads


class TokenPayload(BaseModel):
    iss: str = Field(...)
    sub: Union[str, int] = Field(...)


class UserTokenPayload(TokenPayload):
    user_id: int = Field(...)
    username: EmailStr = Field(...)
    disabled: bool = Field(...)


class PasswordResetPayload(UserTokenPayload):
    iss: str = Field(settings.token.password_reset_iss, const=True)


class AccessTokenPayload(UserTokenPayload):
    iss: str = Field(settings.token.access_iss, const=True)
    confirmed: bool = Field(...)


class ConfirmTokenPayload(UserTokenPayload):
    iss: str = Field(settings.token.confirm_iss, const=True)


class ClientTokenPayload(TokenPayload):
    iss: str = Field(settings.token.client_iss, const=True)
    client_id: Union[str, int] = Field(...)
    user_id: Union[str, int] = Field(...)


# Tokens


class TokenChecked(BaseModel):
    token: str = Field(...)
    payload: TokenPayload = Field(...)


class AccessTokenChecked(TokenChecked):
    payload: AccessTokenPayload = Field(...)


class ConfirmTokenChecked(TokenChecked):
    payload: ConfirmTokenPayload = Field(...)


class PasswordResetChecked(TokenChecked):
    payload: PasswordResetPayload = Field(...)


class RefreshAccessTokenChecked(AccessTokenChecked):
    session: Session = Field(...)


class ClientTokenChecked(TokenChecked):
    payload: ClientTokenPayload = Field(...)


# Generics


TokenPayloadType = TypeVar('TokenPayloadType', bound=TokenPayload)
TokenCheckedType = TypeVar('TokenCheckedType', bound=TokenChecked)
