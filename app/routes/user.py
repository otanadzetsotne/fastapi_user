from fastapi import APIRouter, Depends, HTTPException

from .. import crud
from ..utils import security
from ..utils.randomizer import registration_confirmation_code
from ..dependencies.user import user_not_exist
from ..dependencies.settings import get_settings
from ..schemas import UserBase, UserData


router = APIRouter(prefix='/user')
password_context = security.PasswordContext()


@router.post(path='/register', response_model=UserBase)
async def register(
        user=Depends(user_not_exist),
):
    # Hash password
    password_hash = password_context.hash(user.password)
    # Create user object for DB
    user_db = UserData(**user.dict(), password_hash=password_hash)
    # Insert user to DB
    user_db = await crud.user.create(user_db)

    # TODO: confirmation code send

    return user_db


@router.get('/confirm')
async def confirm():
    pass


# @router.post('/login', response_model=TokenOut)
# def login():
#     pass


# @router.post('/test')
# def test():
#     pass
