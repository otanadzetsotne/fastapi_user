from datetime import datetime

from fastapi import APIRouter, Request, Depends

from ..dependencies.settings import Settings, get_settings
from ..dependencies.user import user_valid_auth
from ..dependencies.db import get_db_session
from ..dependencies.client import client_not_expired
from ..crud import CRUDClient
from ..schemas import ClientData, ClientSecret
from ..utils.security import Client


router_client = APIRouter(prefix='/client')
settings: Settings = get_settings()


@router_client.get('/', response_model=ClientSecret)
async def secret_get(
        token=Depends(user_valid_auth),
        db=Depends(get_db_session),
):
    return await CRUDClient.get_by_user_id(db, token.user.id)


@router_client.post('/', response_model=ClientSecret)
async def create_secret(
        token=Depends(user_valid_auth),
        db=Depends(get_db_session),
):
    client_expires = datetime.utcnow() + settings.token.client_expires
    client_secret = Client.secret(
        length=settings.token.client_length,
        entropy=settings.token.client_entropy,
    )

    client = ClientData(
        user_id=token.user.id,
        secret=client_secret,
        expires=client_expires,
    )

    await CRUDClient.delete_by_user_id(db, token.user.id)
    return await CRUDClient.create(db, client)


@router_client.get('/')
async def delete_secret(
        token=Depends(user_valid_auth),
        db=Depends(get_db_session),
):
    await CRUDClient.delete_by_user_id(db, token.user.id)


@router_client.post('/token')
async def token_secret(
        client=Depends(client_not_expired),
):
    return Client.token(
        client,
        settings.token.algorithm,
        settings.token.client_expires,
        settings.secret.client_key,
    )


@router_client.post('/test')
async def test():
    # TODO: check token and check user validity
    pass
