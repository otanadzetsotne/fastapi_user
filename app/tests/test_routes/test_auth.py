from httpx import AsyncClient

from ..conftest import app_fastapi, base_url


mock_username = 'test@test.com'
mock_name = 'SomeName'
mock_surname = 'SomeSurname'
mock_phone = '+995579159169'
mock_password = 'string'


# For registration
mock_user_register = {
    'username': mock_username,
    'password': mock_password,
}

# For user registration response
mock_user_register_response = {
    'username': mock_username,
    'name': None,
    'surname': None,
    'phone': None,
}


# -------------------------------------------


class TestAuth:
    async def test_registration(self):
        async with AsyncClient(app=app_fastapi, base_url=base_url) as client:
            # TODO: Bug
            response = await client.post(
                '/auth/register',
                content=mock_user_register,
            )

            assert response.status_code == 200
            assert response.json() == mock_user_register_response

    async def test_free(self):
        async with AsyncClient(app=app_fastapi, base_url=base_url) as client:
            response = await client.get('/auth/test_free')

            assert response.status_code == 200
