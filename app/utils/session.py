from functools import cache
from datetime import datetime

from fastapi import Request

from ..schemas import SessionMeta, SessionData
from ..settings import Settings


class SessionUtil:
    @classmethod
    def create(
            cls,
            user_id: int,
            refresh_token: str,
            request: Request,
            settings: Settings,
    ) -> SessionData:
        """
        Create session object
        :param user_id:
        :param refresh_token:
        :param request:
        :param settings:
        :return:
        """

        session_unexpired = cls.create_meta(
            user_id=user_id,
            refresh_token=refresh_token,
            request=request,
        )

        return SessionData(
            **session_unexpired.__dict__,
            expires=datetime.now() + settings.token.refresh_expires,
        )

    @classmethod
    def create_meta(
            cls,
            user_id: int,
            refresh_token: str,
            request: Request,
    ) -> SessionMeta:
        """
        Create session object
        :param user_id:
        :param refresh_token:
        :param request:
        :return:
        """

        return SessionMeta(
            user_id=user_id,
            token=refresh_token,
            agent=cls.create_agent(request),
        )

    @staticmethod
    @cache
    def create_agent(
            request: Request,
    ) -> str:
        """
        Create agent string
        :param request:
        :return:
        """

        host = request.client.host
        user_agent = request.headers.get("user-agent")

        return f'{host} {user_agent}'
