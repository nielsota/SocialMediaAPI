from .. import models
from ..schemas import *
from ..utils import *
from ..database import get_db

from fastapi import Depends, FastAPI, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = UserReturn)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    # hash password
    user.password = hash(user.password)

    # store user
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model=UserReturn)
def get_user(id: int, db: Session = Depends(get_db)):
    
    # get first user
    user = db.query(models.Users).filter(models.Users.id == 1).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id: {id} was not found"
        )
    
    return user


