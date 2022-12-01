from pydoc import cli
from fastapi.testclient import TestClient
from app.database import get_db
from app.main import app
import pytest
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database import Base
from app.models import Post
# from alembic import command
from app.oauth2 import create_access_token

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@\
{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # command.upgrade('heads')
    # command.downgrade('base')
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {'email': 'testuser@test.com',
                'password': 'testuser'}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {'email': 'testuser2@test.com',
                'password': 'testuser2'}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    access_token = create_access_token({'user_id': test_user['id']})
    return access_token
    

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f'Bearer {token}'
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            'title' : 'Test Post 1',
            'content' : 'Test post 1 content',
            'author_id' : test_user['id']
        },
        
        {
            'title' : 'Test Post 2',
            'content' : 'Test post 2 content',
            'author_id' : test_user['id']
        },

        {
            'title' : 'Test Post 3',
            'content' : 'Test post 3 content',
            'author_id' : test_user['id']
        },
       
        {
            'title' : 'Test Post 4',
            'content' : 'Test post 4 content',
            'author_id' : test_user2['id']
        },
        
        {
            'title' : 'Test Post 5',
            'content' : 'Test post 5 content',
            'author_id' : test_user2['id']
        }]

    
    def create_posts_model(post):
        return Post(**post)

    post_map = map(create_posts_model, posts_data)
    posts_list = list(post_map)

    session.add_all(posts_list)
    session.commit()

    posts = session.query(Post).all()
    return posts