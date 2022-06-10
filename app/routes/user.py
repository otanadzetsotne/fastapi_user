from pydantic import EmailStr
from fastapi import (
    Body,
    Request,
    Depends,
    Response,
    APIRouter,
    BackgroundTasks,
)

from .auth import login
from crud import CRUDUser
from schemas import UserBase, UserData, UserUpdatable, AuthTokenOut

from utils.mail import send
from utils.security import HashContext, JWT
from utils.jwt_payload import PayloadCreator

from dependencies.smtp import get_smtp
from dependencies.db import get_db_session
from dependencies.templates import get_templates
from dependencies.settings import Settings, get_settings
from dependencies.user import (
    user_not_exist,
    user_valid_access,
    user_valid_confirm,
    user_password_reset,
    user_update_username,
    user_update_sensitive,
    user_password_reset_request,
)


router_user = APIRouter(prefix='/user')
templates = get_templates()
settings: Settings = get_settings()


@router_user.post('/')
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


@router_user.put('/')
async def update_user_data(
        user_data: UserUpdatable,
        user=Depends(user_valid_access),
        db=Depends(get_db_session),
):
    await CRUDUser.update_by_id(db, user.payload.user_id, **user_data.__dict__)


@router_user.delete('/')
async def disable_user(
        token=Depends(user_update_sensitive),
        db=Depends(get_db_session),
):
    await CRUDUser.update_by_id(db, token.payload.user_id, disabled=True)


@router_user.put('/password/')
async def update_password(
        password_new: str = Body(...),
        token=Depends(user_update_sensitive),
        db=Depends(get_db_session),
):
    password_hash = HashContext.password.hash(password_new)

    await CRUDUser.update_by_id(
        db,
        token.payload.user_id,
        password_hash=password_hash,
    )


@router_user.put('/username/')
async def update_username(
        username_new: EmailStr = Body(...),
        token=Depends(user_update_username),
        db=Depends(get_db_session),
):
    await CRUDUser.update_by_id(
        db,
        token.payload.user_id,
        username=username_new,
        confirmed=False,
    )

    user = await CRUDUser.get_by_id(db, token.payload.user_id)

    # Create confirmation token
    confirm_token = JWT.create(
        PayloadCreator.user_to_confirm(user),
        settings.token.algorithm,
        settings.token.confirm_expires,
        settings.secret.confirm_key,
    )

    # Send confirmation token
    # background_tasks.add_task(send, smtp, user.username, confirm_token)


@router_user.post('/password_reset_request/')
async def password_reset_request(
        background_tasks: BackgroundTasks,
        user=Depends(user_password_reset_request),
        # smtp=Depends(get_smtp),
):
    confirm_token = JWT.create(
        PayloadCreator.user_to_password_reset(user),
        settings.token.algorithm,
        settings.token.confirm_expires,
        settings.secret.confirm_key,
    )

    # Send confirmation token
    # background_tasks.add_task(send, smtp, user.username, confirm_token)


@router_user.post('/password_reset/')
async def password_reset(
        password_new: str = Body(...),
        token=Depends(user_password_reset),
        db=Depends(get_db_session),
):
    user_id = token.payload.user_id
    password_hash = HashContext.password.hash(password_new)
    await CRUDUser.update_by_id(db, user_id, password_hash=password_hash)

