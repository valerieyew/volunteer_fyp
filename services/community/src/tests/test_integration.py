import json
import pytest
import base64
import jwt
import os

secret_key = os.environ.get('COOKIE_JWT_SECRET')


def call(client, path, method='GET', body=None):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    if method == 'POST':
        response = client.post(path, data=json.dumps(body), headers=headers)
    elif method == 'PATCH':
        response = client.patch(path, data=json.dumps(body), headers=headers)
    elif method == 'DELETE':
        response = client.delete(path)
    else:
        response = client.get(path)

    return {
        "json": json.loads(response.data.decode('utf-8')),
        "code": response.status_code
    }


def get_test_token(username, password, role, employee_id, name):
    test_token = jwt.encode({
        'email': username,
        'password': password,
        'role': role,
        'employee_id': employee_id,
        'name': name
    },
        secret_key, algorithm="HS256")
    return test_token


def get_invalid_token(username, password, role, employee_id, name):
    test_token = jwt.encode({
        'email': username,
        'password': password,
        'role': role,
        'employee_id': employee_id,
        'name': name
    },
        "invalid token", algorithm="HS256")
    return test_token


# HEALTH
@pytest.mark.dependency()
def test_health(client):
    result = call(client, '/')
    assert result['code'] == 200


@pytest.mark.dependency()
def test_get_all_posts_fail_not_login(client):
    response = call(client, '/posts/1')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_posts_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/posts/1')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_posts_fail_no_post(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/posts/999')

    assert cookie is not None
    assert response['code'] == 404
    assert response['json']['message'] == "There are no posts."


@pytest.mark.dependency()
def test_get_all_posts_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/posts/1')

    assert cookie is not None
    assert response['code'] == 200


@pytest.mark.dependency()
def test_post_event_posts_fail_not_login(client):
    response = call(client, '/posts/1', 'POST')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_post_event_posts_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/posts/1', 'POST')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_post_event_posts_invalid_event(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/posts/999', 'POST')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "No such event"


@pytest.mark.dependency()
def test_post_event_posts_invalid_body(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "post_title": "Test title"
    }

    response = call(client, '/posts/1', 'POST', body)

    assert cookie is not None
    assert response['code'] == 500
    assert response['json']['message'] == "An error occurred creating post."


@pytest.mark.dependency()
def test_post_event_posts_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "post_title": "Test title",
        "post_message": "Test message"
    }

    response = call(client, '/posts/1', 'POST', body)

    assert cookie is not None
    assert response['code'] == 201
