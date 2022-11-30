from fastapi import (status, HTTPException, Depends, APIRouter)
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import (UserCreateSchema, UserDisplaySchema)
from app.database import get_db
from app.utils import hash_password

user_router = APIRouter(prefix='/users', tags=['Users'])


@user_router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserDisplaySchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    check_email = db.query(User).filter(User.email == user.email).first()

    if check_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f'This email already exists.')

    user.password = hash_password(user.password)
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get('/{id}', response_model=UserDisplaySchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'user with id {id} does not exist!')
    return user
