from fastapi import APIRouter, Request, Depends

from ..crud import CRUDUser, CRUDSession
from ..schemas import AuthTokenOut, SessionAgent

from ..utils.security import JWTAuthPair
from ..utils.session import SessionUtil
from ..utils.jwt_payload import PayloadCreator

from ..dependencies.settings import Settings, get_settings
from ..dependencies.templates import get_templates
from ..dependencies.db import get_db_session
from ..dependencies.user import (
    user_valid_access,
    user_valid_refresh,
    user_login_valid,
)


router_auth = APIRouter(prefix='/auth')
templates = get_templates()
settings: Settings = get_settings()


@router_auth.post('/login/', response_model=AuthTokenOut)
async def login(
        request: Request,
        user=Depends(user_login_valid),
        db=Depends(get_db_session),
):
    access_token, refresh_token = JWTAuthPair.create(
        PayloadCreator.user_to_access(user),
        settings.token.algorithm,
        settings.token.access_expires,
        settings.secret.jwt_key,
        settings.secret.refresh_key,
    )

    # Create session
    session = SessionUtil.create(
        user_id=user.id,
        refresh_token=refresh_token,
        request=request,
        settings=settings,
    )

    # Delete session if exists
    await CRUDSession.delete_by_agent(db, SessionAgent(**session.__dict__))

    # Save refresh token session
    await CRUDSession.create(db, session)

    return AuthTokenOut(
        access_token=access_token,
        expires_in=settings.token.access_expires.total_seconds(),
        token_type=settings.token.type,
        refresh_token=refresh_token,
    )


@router_auth.post('/token/', response_model=AuthTokenOut)
async def token_refresh(
        request: Request,
        token=Depends(user_valid_refresh),
        db=Depends(get_db_session),
):
    user = await CRUDUser.get_by_id(db, token.payload.user_id)
    return await login(request, user, db)


@router_auth.get('/test/')
def test(token=Depends(user_valid_access)):
    return token


@router_auth.get('/test_free/')
def test_free():
    return {'result': True}
