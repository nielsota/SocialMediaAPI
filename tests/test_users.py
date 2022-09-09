from fastapi.testclient import TestClient
from jose import jwt
import pytest

from app.main import app
from app import schemas, models

from .database import client, session
from app import schemas
from app.config import settings

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

def test_create_user(client):

    response = client.post('/users/', json={"email": "forrestota@gmail.com", "password": "password123"})

    # check return code
    assert response.status_code == 201

    # perform schema validation
    new_user = schemas.UserReturn(**response.json())

    # check email
    new_user.email = "forrestota@gmail.com"

def test_login_user(client, test_user):

    response = client.post('/login', data={"username": test_user["email"], "password": test_user["password"]})
    assert response.status_code == 200

    # schema validate the response
    login_response = schemas.Token(**response.json())

    # decode the token
    decoded_access_token = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    print(decoded_access_token)
    print(test_user)

    # check id is correct
    #assert test_user['id'] == decoded_access_token.get['user_id']

