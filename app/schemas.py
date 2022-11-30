from datetime import datetime
from typing import Union
from pydantic import BaseModel, EmailStr, conint


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str

    
class UserDisplaySchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    
class TokenData(BaseModel):
    id: Union[str, None] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

    
class PostDisplaySchema(PostBase):
    id: int
    created_at: datetime
    author_id: int
    author: UserDisplaySchema

    class Config:
        orm_mode = True
    

class PostOut(BaseModel):
    Post: PostDisplaySchema
    votes: int

    class Config:
        orm_mode = True


class PostCreateSchema(PostBase):
    pass


class VoteSchema(BaseModel):
    post_id: int
    dir: conint(le=1)
