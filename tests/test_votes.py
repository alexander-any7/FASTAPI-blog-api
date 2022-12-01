import pytest
from app.models import Vote

@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = Vote(post_id=test_posts[3].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post_success(test_posts, authorized_client, test_user):
    response = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'dir': 1})
    assert response.status_code == 201


def test_vote_twice_post(test_posts, authorized_client, test_vote):
    response = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'dir': 1})
    assert response.status_code == 409


def test_vote_not_exist_post(authorized_client):
    response =  authorized_client.post('/vote/', json={'post_id': 87654, 'dir': 1})
    assert response.status_code == 404


def test_delete_vote(test_posts, authorized_client, test_vote):
    response = authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'dir': 0})
    assert response.status_code == 201


def test_delete_not_exist_post(authorized_client):
    response =  authorized_client.post('/vote/', json={'post_id': 987884, 'dir': 0})
    assert response.status_code == 404


def test_delete_not_exist_vote(authorized_client, test_posts):
    response =  authorized_client.post('/vote/', json={'post_id': test_posts[3].id, 'dir': 0})
    assert response.status_code == 404


def test_vote_unauthorized_user(test_posts, client):
    response = client.post('/vote/', json={'post_id': test_posts[3].id, 'dir': 1})
    assert response.status_code == 401