from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext


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
            payload: dict,
            jwt_algorithm: str,
            jwt_expires: timedelta,
            jwt_key: str,
    ) -> str:
        """
        Create jwt token string with encoded data
        """

        # Prepare data
        to_encode = payload.copy()
        expire = datetime.utcnow() + jwt_expires
        to_encode.update({'exp': expire})

        # Create JWT
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=jwt_key,
            algorithm=jwt_algorithm,
        )

        return encoded_jwt


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
        return HashContext.token.verify(
            jwt_token + refresh_key,
            refresh_token,
        )
