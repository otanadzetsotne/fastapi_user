from fastapi.testclient import TestClient
from app.main import app_fastapi


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
    client = TestClient(app_fastapi)

    def test_registration(self):
        response = self.client.post('/auth/register', json=mock_user_register)
        assert response.status_code == 200
        assert response.json() == mock_user_register_response

    def test_free(self):
        response = TestClient(app_fastapi).get('/auth/test_free')
        assert response.status_code == 200
        assert response.json() == {'result': True}
