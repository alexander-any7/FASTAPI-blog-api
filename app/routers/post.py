from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import Session
from app.models import Post, Vote, User
from app.schemas import (PostBase, PostCreateSchema, PostDisplaySchema, PostOut)
from app.database import get_db
from app.oauth2 import get_current_user

post_router = APIRouter(prefix='/posts', tags=['Posts'])


@post_router.get('/', response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: int = Depends(get_current_user),
              limit: int = 5, skip: int = 0, search: Optional[str] = ''):
    #
    posts = db.query(Post, func.count(Vote.post_id).label('votes')) \
        .join(Vote, Post.id == Vote.post_id, isouter=True) \
        .group_by(Post.id).filter(Post.title.contains(search)).order_by(asc(Post.id)).limit(limit).offset(skip).all()
    return posts


@post_router.get('/user/{id}', response_model=List[PostOut])  # gets all posts by a specific user
def get_user_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User with id of {id} was not found!')

    posts = db.query(Post, func.count(Vote.post_id).label('votes')) \
        .join(Vote, Post.id == Vote.post_id, isouter=True) \
        .group_by(Post.id).filter(Post.author_id == user.id).order_by(desc(Post.id)).all()
    
    return posts


@post_router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostDisplaySchema)
def create_post(post: PostCreateSchema, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = Post(**post.dict(), author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@post_router.get('/{id}', response_model=PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post = db.query(Post, func.count(Vote.post_id).label('votes')) \
        .join(Vote, Post.id == Vote.post_id, isouter=True) \
        .group_by(Post.id).filter(Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id of {id} was not found!')
    return post


@post_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id of {id} does not exist!')

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@post_router.put('/{id}', response_model=PostDisplaySchema)
def update_post(id: int, updated_post: PostBase, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id of {id} does not exist!')

    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not authorized to perform requested action')

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
