from schemas import (
    User,
    Client,
    AccessTokenPayload,
    ConfirmTokenPayload,
    ClientTokenPayload,
    PasswordResetPayload,
)


class PayloadCreator:
    @staticmethod
    def user_to_access(user: User) -> AccessTokenPayload:
        return AccessTokenPayload(
            sub=user.id,
            user_id=user.id,
            username=user.username,
            disabled=user.disabled,
            confirmed=user.confirmed,
        )

    @staticmethod
    def user_to_confirm(user: User) -> ConfirmTokenPayload:
        return ConfirmTokenPayload(
            sub=user.id,
            user_id=user.id,
            username=user.username,
            disabled=user.disabled,
        )

    @staticmethod
    def user_to_password_reset(user: User) -> PasswordResetPayload:
        return PasswordResetPayload(
            sub=user.id,
            user_id=user.id,
            username=user.username,
            disabled=user.disabled
        )

    @staticmethod
    def client_to_client(client: Client) -> ClientTokenPayload:
        return ClientTokenPayload(
            sub=client.id,
            client_id=client.id,
            user_id=client.user_id,
        )
