from fastapi.testclient import TestClient
from jose import jwt
import pytest

from app.main import app
from app.config import settings

from app import schemas, models

@pytest.fixture()
def test_user(client):
    
    user_data = {"email": "testuser@gmail.com", "password": "password123"}
    response = client.post('/users/', json=user_data)
    
    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    
    return new_user

def test_root(client):

    response = client.get('/')
    assert response.status_code == 200
    assert response.json().get('message') == 'Welcome to the statespacing API!'

def test_login_user(client, test_user):

    response = client.post('/login', data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200

    # schema validate the response
    login_response = schemas.Token(**response.json())

    # decode the token
    decoded_access_token = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])

    # check id is correct
    assert test_user['id'] == decoded_access_token['user_id']

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('forrestota@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('forrestota@gmail.com', None, 422) ])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post('/login', data={"username": email, "password": password})
    assert response.status_code == status_code
