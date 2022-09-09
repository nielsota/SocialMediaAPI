from fastapi.testclient import TestClient
import pytest

from app.main import app
from app import schemas, models
from app.config import settings
from app.database import get_db
from app.database import Base

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
