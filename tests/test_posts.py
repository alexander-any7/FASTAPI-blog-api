from dataclasses import dataclass
import pytest
from app.routers.post import update_post
from app.schemas import PostCreateSchema, PostDisplaySchema, PostOut
from app.models import Post



#----------------------Get All Posts----------------------------------------#
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')
    def validate(post):
        return PostOut(**post)

    post_map = map(validate, response.json())
    posts_list = list(post_map)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200
    assert posts_list[0].Post.id == test_posts[0].id
    # assert posts_list[0].Post.title == test_posts[0].title
    # assert posts_list[0].Post.content == test_posts[0].content
    # assert posts_list[0].Post.created_at == test_posts[0].created_at
    # assert posts_list[0].Post.author_id == test_posts[0].author_id


def test_unauthorized_user_get_all_posts(test_posts, client):
    response = client.get('/posts/')
    response_data = response.json()
    assert response.status_code == 401
    # assert response_data['detail'] == "Not authenticated"


#----------------------Get One Post----------------------------------------#
def test_unauthorized_user_get_one_posts(test_posts, client):
    response = client.get(f'/posts/{test_posts[0].id}')
    response_data = response.json()
    assert response.status_code == 401
    # assert response_data['detail'] == "Not authenticated"

def test_get_post_non_exist(test_posts, authorized_client):
    response = authorized_client.get('/posts/88888')
    response_data = response.json()
    assert response.status_code == 404
    

def test_get_one_post_success(test_posts, authorized_client):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = PostOut(**response.json())
    assert post.Post.title == test_posts[0].title


#----------------------Create a Post----------------------------------------#
@pytest.mark.parametrize('title, content, published', [
    ('Test Post 1', 'Test content 1', False),
    # ('Test Post 2', 'Test content 2', True),
    # ('Test Post 3', 'Test content 3', False),
    # ('Test Post 4', 'Test content 4', True)
])


def test_create_post(authorized_client, test_posts, title, content, published, test_user):
    response = authorized_client.post('/posts/',
                json={"title": title, "content": content, 'published': published})
    new_post = PostDisplaySchema(**response.json())
    assert new_post.published == published
    assert new_post.content == content
    assert new_post.title == title
    assert new_post.author_id == test_user['id']
    assert response.status_code == 201


def test_create_post_default_published_true(authorized_client, test_posts, test_user):
    response = authorized_client.post('/posts/',
                json={"title": 'Test Post 1', "content": 'Test Post 1 content'})
    new_post = PostDisplaySchema(**response.json())
    assert new_post.published == True
    assert response.status_code == 201

def test_unauthorized_user_create_post(test_posts, client, test_user):
    response = client.post('/posts/',
                json={"title": 'Test Post 1', "content": 'Test Post 1 content'})
    assert response.status_code == 401


#----------------------Delete a Post----------------------------------------#
def test_user_delete_post_success(test_posts, authorized_client, test_user):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204
    

def test_unauthorized_user_delete_post(test_posts, client, test_user):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_user_delete_post_non_exist(test_posts, authorized_client, test_user):
    response = authorized_client.delete('/posts/098765')
    assert response.status_code == 404


def test_user_delete_other_user_post(test_posts, authorized_client, test_user):
    response = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert response.status_code == 403


#----------------------Update a Post----------------------------------------#
update_data = {
    "title": 'Updated Post 1',
    "content": 'Updated Post 1 content'
    }


def test_user_update_post_success(test_posts, authorized_client, test_user):
    response = authorized_client.put(f'/posts/{test_posts[0].id}',
    json=update_data)
    updated_post = PostDisplaySchema(**response.json())
    assert response.status_code == 200
    assert updated_post.title == update_data['title']
    assert updated_post.content == update_data['content']


def test_unauthorized_user_update_post(test_posts, client, test_user):
    response = client.put(f'/posts/{test_posts[0].id}',
                json=update_data)
    assert response.status_code == 401


def test_user_update_post_non_exist(test_posts, authorized_client, test_user):
    response = authorized_client.put('/posts/9878765',
                json=update_data)
    assert response.status_code == 404


def test_user_update_other_user_post(test_posts, authorized_client, test_user, test_user2):
    response = authorized_client.put(f'/posts/{test_posts[3].id}',
                json=update_data)
    assert response.status_code == 403
