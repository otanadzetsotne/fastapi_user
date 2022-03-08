from fastapi import APIRouter, Request, Depends, BackgroundTasks

from ..crud import CRUDUser, CRUDSession
from ..utils.security import HashContext, JWT, JWTAuthPair
from ..utils.session import SessionUtil
from ..utils.mail import send
from ..utils.jwt_payload import PayloadCreator
from ..dependencies.smtp import get_smtp
from ..dependencies.settings import Settings, get_settings
from ..dependencies.templates import get_templates
from ..dependencies.db import get_db_session
from ..dependencies.user import (
    user_not_exist,
    user_valid_access,
    user_valid_refresh,
    user_valid_confirm,
    user_login_valid,
)
from ..schemas import (
    UserBase,
    UserData,
    AuthTokenOut,
    SessionAgent,
)


router_auth = APIRouter(prefix='/auth')
templates = get_templates()
settings: Settings = get_settings()


@router_auth.post('/register', response_model=UserBase)
async def register(
        background_tasks: BackgroundTasks,
        user=Depends(user_not_exist),
        db=Depends(get_db_session),
        # smtp=Depends(get_smtp),
):
    # Hash password
    password_hash = HashContext.password.hash(user.password)
    # Create user object for DB
    user_db = UserData(**user.dict(), password_hash=password_hash)
    # Insert user to DB
    user = await CRUDUser.create(db, user_db)

    # Create confirmation token
    confirm_token = JWT.create(
        PayloadCreator.user_to_confirm(user),
        settings.token.algorithm,
        settings.token.confirm_expires,
        settings.secret.confirm_key,
    )

    # Send confirmation token
    # background_tasks.add_task(send, smtp, user.username, confirm_token)

    return user


@router_auth.post('/login')
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


@router_auth.post('/token')
async def token_refresh(
        request: Request,
        token=Depends(user_valid_refresh),
        db=Depends(get_db_session),
):
    user = await CRUDUser.get_by_id(db, token.payload.user_id)
    return await login(request, user, db)


@router_auth.get('/confirm/{token}')
async def confirm(
        request: Request,
        token=Depends(user_valid_confirm),
        db=Depends(get_db_session),
):
    # User DB id
    user_id = token.payload.user_id

    # Update user and select for login path operation
    await CRUDUser.update_by_id(db, user_id, confirmed=True)
    user = await CRUDUser.get_by_id(db, user_id)

    # Login and return tokens
    return await login(request, user, db)


@router_auth.get('/test')
def test(token=Depends(user_valid_access)):
    return token


@router_auth.get('/test_free')
def test_free():
    return {'result': True}
