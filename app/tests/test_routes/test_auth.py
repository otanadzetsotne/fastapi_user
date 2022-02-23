from ..conftest import client


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
    def test_registration(self):
        response = client.post(
            '/auth/register',
            json=mock_user_register,
        )

        assert response.status_code == 200,\
            'Wrong status code'

        assert response.json() == mock_user_register_response,\
            'Incorrect response'
