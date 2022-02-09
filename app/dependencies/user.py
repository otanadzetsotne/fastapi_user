from functools import cache

from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)

from .. import schemas
from .. import crud
from ..utils.security import PasswordContext
# from ..schemas import UserCreate, User, TokenOut
# from app.utils.security import PasswordContext
# from settings import Settings

# from config import Settings
# from src.dependencies.settings import (
#     Settings,
#     get_settings,
# )
# from src.dtypes import (
#     User,
#     UserDB,
#     TokenData,
# )
# from src.exceptions import (
#     InactiveUserError,
#     UsernameOrPasswordError,
#     CredentialsError,
# )


# oauth2_scheme = OAuth2PasswordBearer(
#     tokenUrl='token',
# )


# TODO: удалить
# fake_users_db = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # "secret"
#         "disabled": False,
#     },
# }


# async def get_connection():
#     connection = True
#     return connection


# TODO: унести
# async def get_user(
#         username: str,
# ) -> UserDB:
#     if username in fake_users_db:
#         user_dict = fake_users_db[username]
#         return UserDB(**user_dict)


# @cache
# def get_settings() -> Settings:
#     return Settings()


# async def user_token_valid(
#         token: str = Depends(oauth2_scheme),
#         settings: Settings = Depends(get_settings),
# ) -> User:
#     """
#     Get current user from jwt token
#     """
#
#     try:
#         # Decode data from token
#         payload = jwt.decode(
#             token=token,
#             key=settings.secret.key_token,
#             algorithms=[settings.token.algorithm],
#         )
#         # Store username in token subject
#         username: str = payload.get('sub')
#
#         if username is None:
#             raise CredentialsError
#
#         token_data = TokenData(username=username)
#
#     except JWTError:
#         raise CredentialsError
#
#     # Get user entity
#     user = await get_user(token_data.username)
#
#     if not user:
#         raise CredentialsError
#
#     return user


# async def user_active(
#         user: User = Depends(user_token_valid),
# ) -> User:
#     """
#     Check if current user is activated
#     :param user: User object
#     """
#
#     if user.disabled:
#         raise InactiveUserError
#
#     return user


# async def user_authenticate(
#         form_data: OAuth2PasswordRequestForm = Depends(),
#         password_context: PasswordContext = Depends(),
# ) -> User:
#     """
#     Check if user credentials are correct
#     """
#
#     user = await get_user(form_data.username)
#     user = await crud.user.get_by_email(form_data.)
#
#     if not user:
#         raise UsernameOrPasswordError
#
#     if not password_context.verify(form_data.password, user.password_hash):
#         raise UsernameOrPasswordError
#
#     return user


@cache
def get_password_context() -> PasswordContext:
    return PasswordContext()


async def user_not_exist(
        user: schemas.UserIn,
) -> schemas.UserIn:
    """
    Check if user with gotten email not exists
    """

    user_db = await crud.user.get_by_username(user.username)

    if user_db:
        raise HTTPException(
            status_code=400,
            detail='Username already registered',
        )

    user_db = await crud.user.get_by_email(user.email)

    if user_db:
        raise HTTPException(
            status_code=400,
            detail='Email already registered',
        )

    return user
