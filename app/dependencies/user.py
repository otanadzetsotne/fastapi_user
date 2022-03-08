from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from .db import get_db_session
from .token import jwt_auth_checked, jwt_refresh_checked, jwt_confirm_checked
from ..crud import CRUDUser
from ..utils.security import HashContext
from ..schemas import (
    User,
    UserIn,
    AccessTokenChecked,
    RefreshAccessTokenChecked,
    ConfirmTokenChecked,
)
from ..exceptions import (
    UserAlreadyExist,
    InactiveUser,
    InvalidCredentials,
    UnconfirmedUser,
)


def raise_disabled(disabled: bool) -> None:
    if disabled:
        raise InactiveUser


def raise_confirmed(confirmed: bool) -> None:
    if not confirmed:
        raise UnconfirmedUser


async def user_login_valid(
        db=Depends(get_db_session),
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> User:
    # Get user
    user = await CRUDUser.get_by_username(db, form_data.username)

    # Check if user exists
    if user is None:
        raise InvalidCredentials

    # Is password valid
    is_password_valid = HashContext.password.verify(
        form_data.password,
        user.password_hash,
    )

    if not is_password_valid:
        raise InvalidCredentials

    raise_disabled(user.disabled)
    raise_confirmed(user.confirmed)

    return user


# Using for registration validation
async def user_not_exist(
        user: UserIn,
        db=Depends(get_db_session),
) -> UserIn:
    """
    Check if user with gotten email not exists
    """

    user_db = await CRUDUser.get_by_username(db, user.username)

    if user_db:
        raise UserAlreadyExist

    return user


async def user_valid_refresh(
        token: RefreshAccessTokenChecked = Depends(jwt_refresh_checked),
) -> RefreshAccessTokenChecked:
    raise_disabled(token.payload.disabled)
    raise_confirmed(token.payload.confirmed)
    return token


async def user_valid_access(
        token: AccessTokenChecked = Depends(jwt_auth_checked),
) -> AccessTokenChecked:
    raise_disabled(token.payload.disabled)
    raise_confirmed(token.payload.confirmed)
    return token


async def user_valid_confirm(
        token: ConfirmTokenChecked = Depends(jwt_confirm_checked),
) -> ConfirmTokenChecked:
    raise_disabled(token.payload.disabled)
    return token
