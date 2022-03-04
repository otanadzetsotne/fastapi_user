from fastapi import APIRouter, Request, Depends, BackgroundTasks
from pydantic import EmailStr

from ..crud import CRUDUser, CRUDSession
from ..utils.security import HashContext, JWT, JWTAuthPair
from ..utils.randomizer import Randomizer
from ..utils.session import SessionUtil
from ..utils.mail import send
from ..dependencies.smtp import get_smtp, SMTP
from ..dependencies.settings import Settings, get_settings
from ..dependencies.templates import get_templates
from ..dependencies.db import get_db_session
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


@router_auth.post('/register', response_model=UserBase)
async def register(
        background_tasks: BackgroundTasks,
        user=Depends(user_not_exist),
        db=Depends(get_db_session),
        smtp=Depends(get_smtp),
):
    # Hash password
    password_hash = HashContext.password.hash(user.password)
    # Create user object for DB
    user_db = UserData(**user.dict(), password_hash=password_hash)
    # Insert user to DB
    user = await CRUDUser.create(db, user_db)

    # Create confirmation token
    payload = {'sub': user.username, 'user_id': user.id}
    confirm_token = JWT.create(
        payload,
        settings.token.algorithm,
        settings.token.confirm_expires,
        settings.secret.confirm_key,
    )
    # Send confirmation token
    background_tasks.add_task(send, smtp, user.username, confirm_token)

    return user


@router_auth.post('/login')
async def login(
        request: Request,
        user=Depends(user_valid_password),
        db=Depends(get_db_session),
):
    access_token, refresh_token = JWTAuthPair.create(
        user,
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

    return TokenOut(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.token.type,
    )


@router_auth.post('/token')
async def token_refresh(
        request: Request,
        token=Depends(user_valid_refresh),
        db=Depends(get_db_session),
):
    return await login(request, token.user, db)


@router_auth.get('/confirm/{token}')
async def confirm(
        request: Request,
        token=Depends(user_valid_confirmation),
        db=Depends(get_db_session),
):
    return await login(request, token.user, db)


@router_auth.get('/test')
def test(user=Depends(user_valid_auth)):
    return user


@router_auth.get('/test_free')
def test_free():
    return {'result': True}
