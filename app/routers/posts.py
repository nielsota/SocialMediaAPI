from .. import models
from ..schemas import *
from ..utils import *
from ..database import get_db
from ..oauth2 import *

from fastapi import Depends, FastAPI, HTTPException, status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# second path operation - reads methods from top to bottom
#@router.get("/", response_model=List[PostResponseV2])
@router.get("/", response_model=List[PostResponseV2])
def get_posts(
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = ""
):

    # interesting mechanics: the result is stored in cursor. The name is an analogy for how it functions
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))\
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)\
            .group_by(models.Posts.id)\
                .filter(func.lower(Posts.title).contains(func.lower(search)))\
                    .limit(limit=limit)\
                        .offset(skip)\
                            .all()

    return posts


# first post request - make a variable named payload of type dict that defaults to a fastapi body
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
    ):

    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #    (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    
    # need to commit like a git repo
    #conn.commit()

    dict_new_post = post.dict()
    dict_new_post["user_id"] = current_user.id
    
    new_post = models.Posts(**dict_new_post)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) # get the auto-completed id and created_at

    return new_post


@router.get("/{id}", response_model=PostResponseV2)
def get_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
    ):
    
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()

    post = db.query(models.Posts, func.count(models.Votes.post_id).label("votes"))\
        .join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True)\
            .group_by(models.Posts.id)\
                .first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id: {id} was not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
    ):
    
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    
    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id: {id} was not found"
        )
    
    if current_user.id != post_query.first().user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only delete your own posts!"
        )
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return {"message": f"post with id: {id} was deleted"}


@router.put("/{id}", response_model=PostResponse)
def update_post(
    id: int, 
    post: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: TokenData = Depends(get_current_user)
):
    
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    query = post_query.first()
    
    if query is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= f"post with id: {id} was not found"
        )

    if current_user.id != post_query.first().user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You can only delete your own posts!"
        )

    query.update(post.dict(), synchronize_session=False)
    db.commit()

    return query.first()