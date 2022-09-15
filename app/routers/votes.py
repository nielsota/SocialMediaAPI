from .. import models
from ..schemas import *
from ..utils import *
from ..database import get_db
from ..oauth2 import *

from fastapi import Depends, FastAPI, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/vote",
    tags=['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(
    vote: Vote,
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
    ):

    # check if post exists in post database
    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if post is None:
        print('here')
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID: {vote.post_id} does not exist"
            )

    # add vote 
    if vote.direction == 1:
        
        # check if user has not already voted on this post
        old_vote = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id).first()
        if old_vote is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already upvoted this post"
            )

        # add vote to database 
        dict_vote = {"post_id": vote.post_id, "user_id": current_user.id}
        new_vote = models.Votes(**dict_vote)
        db.add(new_vote)
        db.commit()

        return {"message": f"Created upvote for post {vote.post_id}"}

    else:
        
        # check if record of user is present
        old_vote = db.query(models.Votes).filter(models.Votes.user_id == current_user.id, models.Votes.post_id == vote.post_id)
        if old_vote.first() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="You never upvoted this post"
            )
        
        # delete vote if present
        old_vote.delete(synchronize_session=False)
        db.commit()

        return {"message": f"Vote for post with id: {vote.post_id} was deleted"}

