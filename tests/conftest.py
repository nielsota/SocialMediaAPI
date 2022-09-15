"""
conftest automatically scopes fixtures, makes fixtures file package specific.
"""

from venv import create
from fastapi.testclient import TestClient
import pytest

from app.main import app
from app import schemas, models
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_ALCHEMY_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_testing'

engine = create_engine(SQL_ALCHEMY_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a fixture that drops old tables, recreates them and returns a database session
@pytest.fixture
def session():
    # keep the tables when you're done for debugging
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return TestingSessionLocal()
# using the session variable results in using the testing session

# create a fixture that 1. overrides the get_db method and 2. returns a testing client to perform requests on
@pytest.fixture
def client(session):
    # Dependency
    def override_get_db():
        db = session
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "nielsota@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


### FLOW ###
# create a user using a client connected to a testing database.
# retrieve a jwt token for the user
# add the token to the client to authorize it

# api endpoints depend on get_current_user, which checks the token and returnes the user the token belongs to


@pytest.fixture
def test_user(client):
    user_data = {"email": "forrest@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Posts(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])
    session.commit()
    
    posts = session.query(models.Posts).all()

    return posts
