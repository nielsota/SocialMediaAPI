from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserReturn(UserBase):
    created_at: datetime
    email: EmailStr
    id: int

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    id: int
    user_id: int

    # specify foreign key in the models file
    owner: UserReturn

    # Make response ORM compatible 
    class Config:
        orm_mode = True

class PostResponseV2(BaseModel):
    Posts: PostResponse
    votes: int

    # Make response ORM compatible 
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: Optional[str]


class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1) 