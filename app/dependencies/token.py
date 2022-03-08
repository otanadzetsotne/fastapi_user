from typing import Type
from datetime import datetime

from jose import JWTError, jwt
from fastapi import Request, Header, Depends, Path
from fastapi.security import OAuth2PasswordBearer

from .db import get_db_session
from .settings import get_settings, Settings
from ..crud import CRUDSession
from ..utils.security import JWTRefresh
from ..utils.session import SessionUtil
from ..exceptions import InvalidCredentials, RefreshTokenExpired
from ..schemas import (
    TokenPayloadType,
    TokenCheckedType,
    AccessTokenPayload,
    AccessTokenChecked,
    ConfirmTokenPayload,
    ConfirmTokenChecked,
    ClientTokenPayload,
    ClientTokenChecked,
    RefreshAccessTokenChecked,
)


settings: Settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/login',
)
oauth2_scheme_client = OAuth2PasswordBearer(
    tokenUrl='client/token'
)


class JWTChecker:
    key: str
    algorithms: list[str] = [settings.token.algorithm]
    options: dict = {}
    options_base: dict = {
        'require_sub': True,
        'require_exp': True,
    }

    payload_type: Type[TokenPayloadType]
    token_type: Type[TokenCheckedType]

    def __init__(self, **kwargs):
        self.options = kwargs

    def __call__(self, token: str) -> TokenCheckedType:
        try:
            # Validate token
            payload = jwt.decode(
                token=token,
                key=self.key,
                algorithms=self.algorithms,
                options={**self.options_base, **self.options}
            )
        except JWTError:
            raise InvalidCredentials

        return self.token_type(
            token=token,
            payload=self.payload_type(**payload),
        )


class JWTAuthChecker(JWTChecker):
    key = settings.secret.jwt_key
    payload_type = AccessTokenPayload
    token_type = AccessTokenChecked

    def __call__(
            self,
            token: str = Depends(oauth2_scheme),
    ) -> AccessTokenChecked:
        return super(JWTAuthChecker, self).__call__(token)


jwt_auth_checked = JWTAuthChecker()
jwt_auth_checked_unexpired = JWTAuthChecker(
    verify_exp=False,
    require_exp=False,
)


class JWTConfirmChecker(JWTChecker):
    key = settings.secret.confirm_key
    payload_type = ConfirmTokenPayload
    token_type = ConfirmTokenChecked

    def __call__(
            self,
            token: str = Path(...),
    ) -> ConfirmTokenChecked:
        return super(JWTConfirmChecker, self).__call__(token)


jwt_confirm_checked = JWTConfirmChecker()


class JWTClientChecked(JWTChecker):
    key = settings.secret.client_key
    payload_type = ClientTokenPayload
    token_Type = ClientTokenChecked

    def __call__(
            self,
            token: str = Depends(oauth2_scheme_client),
    ):
        return super(JWTClientChecked, self).__call__(token)


async def jwt_refresh_checked(
        request: Request,
        access_token=Depends(jwt_auth_checked_unexpired),
        refresh_token: str = Header(...),
        db=Depends(get_db_session),
) -> RefreshAccessTokenChecked:
    if not JWTRefresh.verify(
            access_token.token,
            settings.secret.refresh_key,
            refresh_token,
    ):
        raise InvalidCredentials

    session_meta = SessionUtil.create_meta(
        user_id=access_token.payload.user_id,
        refresh_token=refresh_token,
        request=request,
    )

    session = await CRUDSession.get_by_meta(db, session_meta)

    # Check if session exists
    if session is None:
        raise InvalidCredentials

    # Check if session expired
    if session.expires <= datetime.now():
        raise RefreshTokenExpired

    return RefreshAccessTokenChecked(
        **dict(access_token),
        session=session,
    )
