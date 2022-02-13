from datetime import datetime

from fastapi import APIRouter, Request, Depends

from ..database.base import db
from ..crud import CRUDUser, CRUDSession
from ..utils.security import HashContext, JWT, JWTRefresh
from ..utils.randomizer import Randomizer
from ..dependencies.smtp import get_smtp
from ..dependencies.user import user_not_exist
from ..dependencies.user import user_authenticate
from ..dependencies.user import user_active
from ..dependencies.settings import get_settings
from ..dependencies.templates import get_templates
from ..schemas import User, UserBase, UserData, TokenOut, SessionData, SessionAgent, Agent


router = APIRouter(prefix='/user')
templates = get_templates()


@router.post(path='/register', response_model=UserBase)
async def register(
        user=Depends(user_not_exist),
):
    # Hash password
    password_hash = HashContext.password.hash(user.password)
    # Create user object for DB
    user_db = UserData(**user.dict(), password_hash=password_hash)
    # Insert user to DB
    user_db = await CRUDUser.create(db, user_db)

    # TODO: confirmation code send

    return user_db


@router.post('/login')
async def login(
        request: Request,
        user=Depends(user_authenticate),
        settings=Depends(get_settings),
):
    # Create token for user
    access_token = JWT.create(
        {'sub': user.username},
        settings.token.algorithm,
        settings.token.access_expires,
        settings.secret.jwt_key,
    )

    # Refresh token for access token update
    refresh_token = JWTRefresh.create(
        access_token,
        settings.secret.refresh_key,
    )

    # User device entity
    agent = Agent(
        host=request.client.host,
        user_agent=request.headers.get('user-agent')
    )

    # Update session for refresh token
    session_agent = SessionAgent(
        user_id=user.id,
        agent=agent.__str__(),
    )

    # Delete session if exists
    await CRUDSession.delete(db, session_agent)

    # Create new session
    session = SessionData(
        **session_agent.__dict__,
        token=refresh_token,
        expires=datetime.utcnow() + settings.token.refresh_expires,
    )

    # Save refresh token session
    await CRUDSession.create(db, session)

    return TokenOut(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type=settings.token.type,
    )


@router.get('/confirm')
async def confirm():
    pass


@router.post('/test')
def test(user: User = Depends(user_active)):
    return {'message': 'correct'}
