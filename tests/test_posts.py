import pytest
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostResponseV2(**res.json())
    assert post.Posts.id == test_posts[0].id
    assert post.Posts.content == test_posts[0].content
    assert post.Posts.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ('Iron Man', 'Movie about iron man, really cool', True),
    ('Thor', 'Movie about Thor, medium cool', True),
    ('Hulk', 'Movie about the hulk, not cool', False)
])
def test_create_post(authorized_client, test_user, title, content, published):
    
    response = authorized_client.post('/posts/', json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published

    assert test_user['id'] == created_post.user_id


def test_unauthorized_user_delete_Post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/8000000")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403