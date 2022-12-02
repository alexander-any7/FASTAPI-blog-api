from jose import jwt
from app.schemas import Token, UserDisplaySchema
from app.config import settings
from tests.conftest import client
import pytest


# def test_root(client):
#     response = client.get("/")
#     assert response.status_code == 200
#     print(response.json().get('message'))
#     assert response.json().get('message') == 'Hello World!'

def test_create_user(client):
    response = client.post('/users/', json={"email":"test@gmail.com", "password":"test"})
    new_user = UserDisplaySchema(**response.json())
    assert new_user.email == 'test@gmail.com'
    assert response.status_code == 201


def test_login(client, test_user):
    response = client.post('/login', data={"username": test_user['email'], "password": test_user['password']})
    login_response = Token(**response.json())
    token = login_response.access_token
    payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get('user_id')
    assert id == test_user['id']
    login_response.token_type == 'bearer'
    assert response.status_code == 200


@pytest.mark.parametrize('email, password, status_code', [
    ('testuser@test.com', 'testuserw', 403),
    ('testuser@test.comw', 'testuser', 403),
    ('testuser@test.comw', 'testuserw', 403),
    (None, 'testuser', 422),
    ('testuser@test.com', None, 422)
])


def test_failed_login(client, test_user, email, password, status_code):
    response = client.post('/login', data={"username": email, "password": password})
    assert response.status_code == status_code


