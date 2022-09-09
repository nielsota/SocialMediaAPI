
from fastapi import FastAPI

from .schemas import *
from .utils import *
from . import models
from .database import engine
from .routers import posts, users, auth, votes
from .config import *

# don't need this anymore because alembic is taking care of it
# models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# if the API will be used by a specific website, specify the orgins of that website here
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# first path operation
@app.get("/")
def root():
    return {"message": "Welcome to the statespacing API!"}

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)


