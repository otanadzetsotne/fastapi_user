from fastapi import APIRouter, Request, Depends, BackgroundTasks

from .auth import login
from ..crud import CRUDUser
from ..schemas import UserBase, UserData, AuthTokenOut

from ..utils.mail import send
from ..utils.security import HashContext, JWT
from ..utils.jwt_payload import PayloadCreator

from ..dependencies.smtp import get_smtp
from ..dependencies.db import get_db_session
from ..dependencies.templates import get_templates
from ..dependencies.settings import Settings, get_settings
from ..dependencies.user import user_not_exist, user_valid_confirm


router_user = APIRouter(prefix='/user')
templates = get_templates()
settings: Settings = get_settings()


@router_user.post('/', response_model=UserBase)
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


@router_user.get('/confirm/{token}/', response_model=AuthTokenOut)
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
