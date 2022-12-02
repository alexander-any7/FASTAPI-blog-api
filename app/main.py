from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.post import post_router
from app.routers.user import user_router
from app.routers.auth import auth_router
from app.routers.vote import vote_router

# Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)


@app.get('/')
def root():
    return {'message': 'Hello World! Successfully deployed my first API from CI/CD pipeline'}
