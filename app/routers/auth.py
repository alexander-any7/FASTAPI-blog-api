from fastapi import APIRouter, Depends, status, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import Token
from app.models import User
from app.utils import verify
from app.oauth2 import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(tags=['Authentication'])


@auth_router.post('/login', response_model=Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials!')
    
    if not verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid credentials!')
    
    access_token = create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
    
