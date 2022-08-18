from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from requests import Session

from ..database import get_db
from ..schemas import *
from ..models import *
from ..utils import *
from ..oauth2 import *

router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session=Depends(get_db)
    ):
    
    """Logic flow: log in to get a token, token needed for all operations"""
    
    user = db.query(Users).filter(Users.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'invalid credentials'
        )
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'invalid credentials'
        )

    #create token
    acces_token = create_access_token(data={"user_id": user.id})
    
    return {"access_token": acces_token, "token_type": "bearer"}
