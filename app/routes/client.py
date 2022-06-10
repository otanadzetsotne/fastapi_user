from datetime import datetime

from fastapi import APIRouter, Depends

from crud import CRUDClient
from dependencies.settings import Settings, get_settings
from dependencies.user import user_valid_access
from dependencies.db import get_db_session, AsyncSession
from dependencies.client import client_not_expired
from utils.security import JWTClient
from schemas import (
    ClientData,
    ClientSecret,
    ClientTokenPayload,
    ClientTokenOut,
)


router_client = APIRouter(prefix='/client')
settings: Settings = get_settings()


@router_client.get('/', response_model=ClientSecret)
async def secret_get(
        token=Depends(user_valid_access),
        db=Depends(get_db_session),
):
    return await CRUDClient.get_by_user_id(db, token.payload.user_id)


@router_client.post('/', response_model=ClientSecret)
async def create_secret(
        token=Depends(user_valid_access),
        db: AsyncSession = Depends(get_db_session),
):
    client_expires = datetime.utcnow() + settings.token.client_expires
    client_secret = JWTClient.random_secret(
        length=settings.token.client_length,
        entropy=settings.token.client_entropy,
    )

    client = ClientData(
        user_id=token.payload.user_id,
        secret=client_secret,
        expires=client_expires,
    )

    await CRUDClient.delete_by_user_id(db, token.payload.user_id)
    return await CRUDClient.create(db, client)


@router_client.delete('/')
async def delete_secret(
        token=Depends(user_valid_access),
        db=Depends(get_db_session),
):
    await CRUDClient.delete_by_user_id(db, token.payload.user_id)


@router_client.post('/token/')
async def token_secret(
        client=Depends(client_not_expired),
):
    client_payload = ClientTokenPayload(
        sub=client.id,
        client_id=client.id,
        user_id=client.user_id,
    )

    token = JWTClient.token(
        client_payload,
        settings.token.algorithm,
        settings.token.client_expires,
        settings.secret.client_key,
    )

    return ClientTokenOut(
        access_token=token,
        token_type=settings.token.type,
        expires_in=settings.token.client_expires.total_seconds()
    )


@router_client.post('/test/')
async def test():
    # TODO: check token and check user validity
    pass
