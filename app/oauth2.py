from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .schemas import *
from .database import *
from .models import *
from .config import *

# Secret key
# Algorithm
# Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data: dict):
    
    # later will encode header and payload into signature
    to_encode = data.copy()

    # create expiration time
    expire = datetime.utcnow() + timedelta(minutes=30)

    # add expiration date to payload
    to_encode.update({"exp": expire})

    # encode the result
    jwt_code = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return jwt_code

# Check if token is valid, will be created during log in process
def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


# this function will be injected as a dependency for anyone who wants to log in
def get_current_user(
    token: str = Depends(oauth_scheme),
    db: Session = Depends(get_db)):
    '''depending on oathh_scheme means you expect a token to be passed as a bearer'''
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = 'Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = verify_access_token(token, credentials_exception=credentials_exception)

    user = db.query(Users).filter(Users.id == token.id).first()

    return user