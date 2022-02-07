from datetime import datetime
from datetime import timedelta

from jose import jwt
from passlib.context import CryptContext


class PasswordContext:
    def __init__(self):
        self.context = CryptContext(
            schemes=['bcrypt'],
            deprecated='auto',
        )

    def hash(self, password):
        return self.context.hash(password)

    def verify(self, password, password_hash):
        return self.context.verify(password, password_hash)


class JWT:
    @staticmethod
    def create(
            data: dict,
            token_algorithm: str,
            token_expires: timedelta,
            token_secret_key: str,
    ):
        """
        Create jwt token string with encoded data
        """

        # Prepare data
        to_encode = data.copy()
        expire = datetime.utcnow() + token_expires
        to_encode.update({'exp': expire})

        # Create JWT
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=token_secret_key,
            algorithm=token_algorithm,
        )

        return encoded_jwt
