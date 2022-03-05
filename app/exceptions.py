from fastapi import HTTPException


InvalidCredentials = HTTPException(
    status_code=401,
    detail='Invalid credentials',
    headers={"WWW-Authenticate": "Bearer"},
)

UnconfirmedUser = HTTPException(
    status_code=403,
    detail='Not confirmed user',
)

InactiveUser = HTTPException(
    status_code=403,
    detail='Inactive user',
)

UserAlreadyExist = HTTPException(
    status_code=400,
    detail='Username already registered',
)

RefreshTokenExpired = HTTPException(
    status_code=403,
    detail='Refresh token expired',
)

InvalidClient = HTTPException(
    status_code=403,
    detail='Invalid client'
)

ClientExpired = HTTPException(
    status_code=403,
    detail='Client expired'
)
