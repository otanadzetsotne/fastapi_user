from datetime import datetime

from jose import JWTError, jwt
from fastapi import Request, Header, Depends, Path
from fastapi.security import OAuth2PasswordBearer

from .db import get_db_session
from .settings import get_settings, Settings
from .. import schemas
from ..crud import CRUDSession
from ..utils.security import JWTRefresh
from ..utils.session import SessionUtil
from ..exceptions import InvalidCredentials, RefreshTokenExpired


settings: Settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/login',
)


class JWTChecker:
    key: str
    algorithms: list[str] = [settings.token.algorithm]
    options: dict = {}
    options_base: dict = {
        'require_sub': True,
        'require_exp': True,
    }

    def __init__(self, **kwargs):
        self.options = kwargs

    async def __call__(self, token: str) -> schemas.AccessTokenChecked:
        """
        Check if access token is valid
        """

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

        return schemas.AccessTokenChecked(
            token=token,
            payload=payload,
            # user=user,
        )


class JWTAuthChecker(JWTChecker):
    key = settings.secret.jwt_key

    async def __call__(
            self,
            token: str = Depends(oauth2_scheme),
    ) -> schemas.AccessTokenChecked:
        return await super(JWTAuthChecker, self).__call__(token)


jwt_auth_checked = JWTAuthChecker()
jwt_auth_checked_unexpired = JWTAuthChecker(
    verify_exp=False,
    require_exp=False,
)


class JWTConfirmChecker(JWTChecker):
    key = settings.secret.confirm_key

    async def __call__(
            self,
            token: str = Path(...),
    ) -> schemas.AccessTokenChecked:
        return await super(JWTConfirmChecker, self).__call__(token)


jwt_confirm_checked = JWTConfirmChecker(
    verify_exp=False,
    require_exp=False,
)


class JWTRefreshChecker:
    async def __call__(
            self,
            request: Request,
            access_token=Depends(jwt_auth_checked_unexpired),
            refresh_token: str = Header(...),
            db=Depends(get_db_session),
    ) -> schemas.RefreshTokenChecked:
        refresh_token_valid = JWTRefresh.create(
            access_token.token,
            settings.secret.refresh_key,
        )

        if refresh_token != refresh_token_valid:
            raise InvalidCredentials

        session_meta = SessionUtil.create_meta(
            user_id=access_token.payload.get('id'),
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

        return schemas.RefreshTokenChecked(
            **access_token.__dict__,
            session=session,
        )


jwt_refresh_checked = JWTRefreshChecker()
