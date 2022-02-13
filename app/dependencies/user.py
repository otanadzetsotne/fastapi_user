from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from .settings import get_settings, Settings
from .. import schemas
from ..crud import CRUDUser
from ..database.base import db
from ..utils.security import HashContext


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='user/login',
)


async def user_token_valid(
        token: str = Depends(oauth2_scheme),
        settings: Settings = Depends(get_settings),
) -> schemas.User:
    """
    Get current user from jwt token
    """

    try:
        # Decode data from token
        payload = jwt.decode(
            token=token,
            key=settings.secret.jwt_key,
            algorithms=[settings.token.algorithm],
        )
        # Store username in token subject
        username: str = payload.get('sub')

        # TODO: token expires check

        if username is None:
            raise HTTPException(
                status_code=400,
                detail='Invalid credentials',
            )

        token_data = schemas.TokenData(username=username)

    except JWTError:
        raise HTTPException(
            status_code=400,
            detail='Invalid credentials',
        )

    # Get user entity
    user = await CRUDUser.get_by_username(db, token_data.username)

    if not user:
        raise HTTPException(
            status_code=400,
            detail='Invalid credentials',
        )

    return user


async def user_active(
        user: schemas.User = Depends(user_token_valid),
) -> schemas.User:
    """
    Check if current user is activated
    :param user: User object
    """

    if user.disabled:
        raise HTTPException(
            status_code=401,
            detail='User disabled',
        )

    return user


async def user_authenticate(
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.User:
    """
    Check if user credentials are correct
    """

    user = await CRUDUser.get_by_username(db, form_data.username)

    if not user:
        raise HTTPException(
            status_code=400,
            detail='Invalid credentials',
        )

    if not HashContext.password.verify(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail='Invalid credentials',
        )

    return user


async def user_not_exist(
        user: schemas.UserIn,
) -> schemas.UserIn:
    """
    Check if user with gotten email not exists
    """

    user_db = await CRUDUser.get_by_username(db, user.username)

    if user_db:
        raise HTTPException(
            status_code=400,
            detail='Username already registered',
        )

    user_db = await CRUDUser.get_by_email(db, user.email)

    if user_db:
        raise HTTPException(
            status_code=400,
            detail='Email already registered',
        )

    return user
