from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext
from passlib.pwd import genword

from ..schemas import ClientTokenPayload, TokenPayloadType, AccessTokenPayload


class HashContext:
    password = CryptContext(
        schemes=['bcrypt'],
        deprecated='auto',
    )

    token = CryptContext(
        schemes=['bcrypt'],
    )


class JWT:
    @staticmethod
    def create(
            payload: TokenPayloadType,
            jwt_algorithm: str,
            jwt_expires: timedelta,
            jwt_key: str,
    ) -> str:
        """
        Create jwt token string with encoded data
        """

        # Prepare data
        expires = datetime.utcnow() + jwt_expires
        to_encode = dict(payload).copy()
        to_encode.update({'exp': expires})

        # Create JWT
        return jwt.encode(
            claims=to_encode,
            key=jwt_key,
            algorithm=jwt_algorithm,
        )


class JWTRefresh:
    @staticmethod
    def create(
            jwt_token: str,
            refresh_key: str,
    ) -> str:
        payload = jwt_token + refresh_key
        refresh_token = HashContext.token.hash(payload)

        return refresh_token

    @classmethod
    def verify(
            cls,
            jwt_token: str,
            refresh_key: str,
            refresh_token: str,
    ):
        return HashContext.token.verify(jwt_token + refresh_key, refresh_token)


class JWTAuthPair:
    @staticmethod
    def create(
            payload: AccessTokenPayload,
            algorithm: str,
            access_expires: timedelta,
            access_key: str,
            refresh_key: str,
    ) -> tuple[str, str]:
        """
        Create auth token pairs
        :param payload: Payload object with necessary payload data
        :param algorithm: encryption algorithm
        :param access_expires: access token expire time
        :param access_key: access token secret key
        :param refresh_key: refresh token secret key
        :return: access_token and refresh_token
        """

        access = JWT.create(payload, algorithm, access_expires, access_key)
        refresh = JWTRefresh.create(access, refresh_key)

        return access, refresh


class JWTClient:
    @staticmethod
    def random_secret(
            length: int,
            entropy: int,
    ) -> str:
        return genword(length=length, entropy=entropy)

    @staticmethod
    def token(
            payload: ClientTokenPayload,
            algorithm: str,
            client_expires: timedelta,
            client_key: str,
    ):
        return JWT.create(payload, algorithm, client_expires, client_key)
