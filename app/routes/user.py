from fastapi import APIRouter, Depends, HTTPException

from .. import crud
from ..utils.security import JWT
from ..utils.randomizer import registration_confirmation_code
from ..dependencies.user import user_not_exist, get_password_context
from ..dependencies.settings import get_settings
from ..schemas import UserBase, UserData


router = APIRouter(prefix='/user')


@router.post(path='/register', response_model=UserBase)
async def register(
        user=Depends(user_not_exist),
        password_context=Depends(get_password_context)
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


# @router.post('/login')
# async def login_for_access_token(
#         user: User = Depends(user_authenticate),
#         settings: Settings = Depends(get_settings),
# ):
#     Create token for user
    # access_token = JWT.create(
    #     {'sub': user.username},
    #     settings.token.algorithm,
    #     settings.token.expires,
    #     settings.secret.key_token,
    # )
    #
    # return {
    #     'access_token': access_token,
    #     'token_type': settings.token.type,
    # }



# @router.post('/test')
# def test():
#     pass
