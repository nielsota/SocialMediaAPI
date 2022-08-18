###################################################
# File responsible for connecting to the database #
###################################################

from .config import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import time
import psycopg2
from psycopg2.extras import RealDictCursor

SQL_ALCHEMY_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQL_ALCHEMY_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# For reference, not using since migrating to sqlalchemy
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='123', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection established')
        break
    except Exception as error:
        print('Database connection failed')
        print(f'Error: {error}')
        time.sleep(2)

