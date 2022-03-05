from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_db_session
from .token import jwt_auth_checked, jwt_refresh_checked, jwt_confirm_checked
from .. import schemas
from ..crud import CRUDUser
from ..utils.security import HashContext
from ..exceptions import (
    UserAlreadyExist,
    InactiveUser,
    InvalidCredentials,
    UnconfirmedUser,
)


class UserExists:
    async def __call__(self, db, username: str):
        # Get user
        user = await CRUDUser.get_by_username(db, username)

        # Check if user exists
        if user is None:
            raise InvalidCredentials

        return user


class UserActive(UserExists):
    async def __call__(self, db, username: str):
        user = await super(UserActive, self).__call__(db, username)

        if user.disabled:
            raise InactiveUser

        return user


class UserConfirmed(UserActive):
    async def __call__(self, db, username: str):
        user = await super(UserConfirmed, self).__call__(db, username)

        if not user.confirmed:
            raise UnconfirmedUser

        return user


class UserPassword(UserExists):
    async def __call__(
            self,
            db=Depends(get_db_session),
            form_data: OAuth2PasswordRequestForm = Depends(),
    ):
        user = await super(UserPassword, self).__call__(db, form_data.username)

        # Check if password is valid
        is_password_valid = HashContext.password.verify(
            form_data.password,
            user.password_hash,
        )

        # If password is not valid throw exception
        if not is_password_valid:
            raise InvalidCredentials

        return user


# Using for user credentials validation
user_valid_password = UserPassword()


class UserValid:
    user_checker: UserExists

    async def __call__(
            self,
            db: AsyncSession,
            token: schemas.AccessTokenChecked,
    ):
        username = token.payload.get('sub')
        token.user = await self.user_checker.__call__(db, username)

        return token


class UserAuth(UserValid):
    user_checker = UserConfirmed()

    async def __call__(
            self,
            db=Depends(get_db_session),
            access_token=Depends(jwt_auth_checked),
    ):
        return await super(UserAuth, self).__call__(db, access_token)


# Using for access token validation
user_valid_auth = UserAuth()


class UserAuthRefresh(UserValid):
    user_checker = UserConfirmed()

    async def __call__(
            self,
            db=Depends(get_db_session),
            token=Depends(jwt_refresh_checked),
    ):
        return await super(UserAuthRefresh, self).__call__(db, token)


# Using for refresh token validation
user_valid_refresh = UserAuthRefresh()


class UserConfirm(UserValid):
    user_checker = UserActive()

    async def __call__(
            self,
            db=Depends(get_db_session),
            token=Depends(jwt_confirm_checked),
    ):
        return await super(UserConfirm, self).__call__(db, token)


# Using for confirmation token validation
user_valid_confirmation = UserConfirm()


# Using for registration validation
async def user_not_exist(
        user: schemas.UserIn,
        db=Depends(get_db_session),
) -> schemas.UserIn:
    """
    Check if user with gotten email not exists
    """

    user_db = await CRUDUser.get_by_username(db, user.username)

    if user_db:
        raise UserAlreadyExist

    return user


# TODO: We need to refuse to get entire user data from db in jwt validation
#  also, we even need to remove user existence check
