from datetime import datetime

from fastapi import APIRouter, Request, Depends

from ..database.base import db
from ..crud import CRUDUser, CRUDSession
from ..utils.security import HashContext, JWT, JWTRefresh
from ..utils.randomizer import Randomizer
from ..utils.session import SessionUtil
from ..dependencies.settings import Settings, get_settings
from ..dependencies.templates import get_templates
from ..dependencies.user import (
    user_not_exist,
    user_valid_auth,
    user_valid_refresh,
    user_valid_password,
    user_valid_confirmation,
)
from ..schemas import (
    UserBase,
    UserData,
    TokenOut,
    SessionAgent,
)


router_auth = APIRouter(prefix='/auth')
templates = get_templates()
settings: Settings = get_settings()


@router_auth.post(path='/register', response_model=UserBase)
async def register(
        user=Depends(user_not_exist),
):
    # Hash password
    password_hash = HashContext.password.hash(user.password)
    # Create user object for DB
    user_db = UserData(**user.dict(), password_hash=password_hash)
    # Insert user to DB
    user = await CRUDUser.create(db, user_db)

    # TODO: confirmation code send

    # TODO: Return password hash is not safe
    return user


@router_auth.post('/login')
async def login(
        request: Request,
        user=Depends(user_valid_password),
):
    # Payload for jwt token
    payload = {'sub': user.username, 'user_id': user.id}

    # Create token for user
    access_token = JWT.create(
        payload,
        settings.token.algorithm,
        settings.token.access_expires,
        settings.secret.jwt_key,
    )

    # Refresh token for access token update
    refresh_token = JWTRefresh.create(
        access_token,
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

    return TokenOut(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.token.type,
    )


@router_auth.post('/token')
async def token_refresh(token=Depends(user_valid_refresh)):
    return token


@router_auth.get('/confirm')
async def confirm(token=Depends(user_valid_confirmation)):
    return token


@router_auth.post('/test')
def test(user=Depends(user_valid_auth)):
    return user


@router_auth.get('/test_free')
def test_free():
    return {'result': True}
