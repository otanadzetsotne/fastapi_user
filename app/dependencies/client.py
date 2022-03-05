from datetime import datetime

from fastapi import Depends

from .db import get_db_session
from ..crud import CRUDClient
from ..schemas import ClientMeta, Client
from ..exceptions import InvalidClient, ClientExpired


def client_exists(
        user_id: int,
        secret: str,
        db=Depends(get_db_session),
) -> Client:
    client_meta = ClientMeta(user_id=user_id, secret=secret)
    client = await CRUDClient.get_by_client_meta(db, client_meta)

    if not client:
        raise InvalidClient

    return client


def client_not_expired(
        client=Depends(client_exists),
) -> Client:
    if client.expires < datetime.utcnow():
        raise ClientExpired

    return client
