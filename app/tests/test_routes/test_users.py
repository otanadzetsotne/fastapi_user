from ..conftest import client


mock_user_base = {}


def test_route_free():
    response = client.get(
        '/auth/test_free',
    )
    assert response.status_code == 200
