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


@pytest.mark.dependency()
def test_health(client):
    result = call(client, '/')
    assert result['code'] == 200


@pytest.mark.dependency()
def test_get_all_approved_fail_not_login(client):
    response = call(client, '/events')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_approved_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_approved_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_all_pending_fail_not_login(client):
    response = call(client, '/events/pending')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_pending_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/pending')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_pending_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/pending')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_all_rejected_fail_not_login(client):
    response = call(client, '/events/rejected')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_rejected_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/rejected')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_rejected_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/rejected')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_all_proposed_fail_not_login(client):
    response = call(client, '/events/proposed')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_proposed_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/proposed')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_proposed_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/proposed')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_all_enrolled_fail_not_login(client):
    response = call(client, '/events/proposed')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_enrolled_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/proposed')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_enrolled_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/enrolled')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_one_event_fail_not_login(client):
    response = call(client, '/events/1')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_one_event_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/1')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_one_event_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/1')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_event_session_attendees_fail_not_login(client):
    response = call(client, '/events/1/participants')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_event_session_attendees_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/1/participants')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_event_session_attendees_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/1/participants')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_get_user_attendances_fail_not_login(client):
    response = call(client, '/events/1/attendances')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_user_attendances_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/1/attendances')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


def test_get_user_attendances_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    response = call(client, '/events/1/attendances')

    assert response['code'] == 200


@pytest.mark.dependency()
def test_create_event_fail_not_login(client):
    response = call(client, '/events', 'POST')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_create_event_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events', 'POST')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_create_event_invalid_body_event(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    # Missing 'info' key in body
    body = {
        "name": "name",
        "location": "NIL",
        "proposal_details": "details",
        "registration_opens_on": "2022-01-01 00:00:00",
        "registration_closes_on": "2022-01-01 00:00:00",
        "image_url": [
            "test_url1",
            "test_url2"
        ],
        "sessions": [
            {
                "start_time": "2022-01-01 00:00:00",
                "end_time": "2022-01-01 00:00:00",
                "capacity": 50,
                "fill": 0
            },
            {
                "start_time": "2022-01-02 00:00:00",
                "end_time": "2022-01-02 00:00:00",
                "capacity": 51,
                "fill": 0
            }
        ],
        "tags": [
            "tag1",
            "tag2"
        ]
    }

    response = call(client, '/events', 'POST', body)
    assert cookie is not None
    assert response['code'] == 404
    assert response['json'][
        'message'] == "An error occurred creating event. (Lack of required keys in event)"


@pytest.mark.dependency()
def test_create_event_invalid_body_session(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    # Missing 'fill' key in session keys
    body = {
        "name": "name",
        "location": "NIL",
        "proposal_details": "details",
        "info": "info",
        "registration_opens_on": "2022-01-01 00:00:00",
        "registration_closes_on": "2022-01-01 00:00:00",
        "image_url": [
            "test_url1",
            "test_url2"
        ],
        "sessions": [
            {
                "start_time": "2022-01-01 00:00:00",
                "end_time": "2022-01-01 00:00:00",
                "capacity": 50,
            },
            {
                "start_time": "2022-01-02 00:00:00",
                "end_time": "2022-01-02 00:00:00",
                "capacity": 51,
                "fill": 0
            }
        ],
        "tags": [
            "tag1",
            "tag2"
        ]
    }

    response = call(client, '/events', 'POST', body)
    assert cookie is not None
    assert response['code'] == 404
    assert response['json'][
        'message'] == "An error occurred creating event. (Lack of required keys in sessions)"


@pytest.mark.dependency()
def test_create_event_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "name": "name",
        "location": "NIL",
        "proposal_details": "details",
        "info": "info",
        "registration_opens_on": "2022-01-01 00:00:00",
        "registration_closes_on": "2022-01-01 00:00:00",
        "image_url": [
            "test_url1",
            "test_url2"
        ],
        "sessions": [
            {
                "start_time": "2022-01-01 00:00:00",
                "end_time": "2022-01-01 00:00:00",
                "capacity": 50,
                "fill": 0
            },
            {
                "start_time": "2022-01-02 00:00:00",
                "end_time": "2022-01-02 00:00:00",
                "capacity": 51,
                "fill": 0
            }
        ],
        "tags": [
            "tag1",
            "tag2"
        ]
    }

    response = call(client, '/events', 'POST', body)

    assert cookie is not None
    assert response['code'] == 201


@pytest.mark.dependency()
def test_create_session_fail_not_login(client):
    response = call(client, '/events/1/sessions', 'POST')

    assert response['code'] == 404
    assert response['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_create_session_invalid_jwt(client):
    invalid_jwt = get_invalid_token(
        'john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/1/sessions', 'POST')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_create_session_wrong_employee_id(client):
    token = get_test_token('jane.doe@email.com', 'test123',
                           'admin', '000002', 'Jane Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    response = call(client, '/events/1/sessions', 'POST')

    assert cookie is not None
    assert response['code'] == 401
    assert response['json']['message'] == "Wrong employee_id"


@pytest.mark.dependency()
def test_create_session_wrong_body(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "start_time": "2022-02-13 00:00:00",
        "end_time": "2022-02-14 00:00:00"
    }

    response = call(client, '/events/1/sessions', 'POST', body)

    assert cookie is not None
    assert response['code'] == 500
    assert response['json']['message'] == "An error occurred creating session."


@pytest.mark.dependency()
def test_create_session_success(client):
    token = get_test_token('john.doe@email.com', 'test123',
                           'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', token)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "start_time": "2022-02-13 00:00:00",
        "end_time": "2022-02-14 00:00:00",
        "capacity": 22
    }

    response = call(client, '/events/1/sessions', 'POST', body)

    assert cookie is not None
    assert response['code'] == 201
