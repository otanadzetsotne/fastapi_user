from fastapi import APIRouter, Depends

from ..database.base import db
from ..crud import CRUDUser
from ..utils.security import JWT, PasswordContext
from ..utils.randomizer import Randomizer
from ..dependencies.user import user_not_exist
from ..dependencies.user import user_authenticate
from ..dependencies.user import user_active
from ..dependencies.settings import get_settings
from ..schemas import User, UserBase, UserData, TokenOut


router = APIRouter(prefix='/user')


@router.post(path='/register', response_model=UserBase)
async def register(
        user=Depends(user_not_exist),
):
    # Hash password
    password_hash = PasswordContext.hash(user.password)
    # Create user object for DB
    user_db = UserData(**user.dict(), password_hash=password_hash)
    # Insert user to DB
    user_db = await CRUDUser.create(db, user_db)

    # TODO: confirmation code send

    return user_db


@router.post('/login')
async def login_for_access_token(
        user=Depends(user_authenticate),
        settings=Depends(get_settings),
):
    # Create token for user
    access_token = JWT.create(
        {'sub': user.username},
        settings.token.algorithm,
        settings.token.expires,
        settings.secret.jwt_key,
    )

    return TokenOut(
        access_token=access_token,
        token_type=settings.token.type,
    )


@router.get('/confirm')
async def confirm():
    pass


@router.post('/test')
def test(user: User = Depends(user_active)):
    return {'message': 'correct'}
