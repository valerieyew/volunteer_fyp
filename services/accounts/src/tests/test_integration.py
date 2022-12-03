import json
import pytest
import base64
import jwt

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

def get_invalid_token(username, password, role, employee_id, name):
    test_token = jwt.encode({
            'email': username,
            'password': password,
            'role': role,
            'employee_id': employee_id,
            'name': name
        },
            "invalid secret", algorithm="HS256")
    return test_token

# HEALTH

@pytest.mark.dependency()
def test_health(client):
    result = call(client, '/')
    assert result['code'] == 200

# LOGIN

@pytest.mark.dependency()
def test_login_success(client):
    valid_credentials = base64.b64encode(b"sova@email.com:sova123").decode("utf-8")
    result = client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
        })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = {
        "json": json.loads(result.data.decode('utf-8')),
        "code": result.status_code
    }

    assert result['code'] == 200
    assert result['json']['message'] == {
        "email": "sova@email.com",
        "employee_id": "000003",
        "name": "Sova",
        "phone_number": "77777777",
        "role": "user"
    }
    assert cookie is not None


@pytest.mark.dependency()
def test_login_fail_wrong_pw(client):
    valid_credentials = base64.b64encode(b"sova@email.com:wrongpw").decode("utf-8")
    result = client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
        })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = {
        "json": json.loads(result.data.decode('utf-8')),
        "code": result.status_code
    }

    assert result['code'] == 404
    assert result['json']['message'] == "Account doesn't exist"
    assert cookie is None

# LOGOUT

@pytest.mark.dependency()
def test_logout_success(client):
    valid_credentials = base64.b64encode(b"sova@email.com:sova123").decode("utf-8")
    result = client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
        })

    result = call(client, '/logout', 'POST')

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    assert result['code'] == 200
    assert cookie is None

# Create account

@pytest.mark.dependency()
def test_create_account_fail_not_login(client):
    result = call(client, '/register', 'POST')

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    assert result['code'] == 404
    assert result['json']['message'] == "Not logged in"
    assert cookie is None


@pytest.mark.dependency()
def test_create_account_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token('john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "employee_id": "123456",
        "name": "test",
        "phone_number": "12345678",
        "email": "test@test.com",
        "password": "test123"
    }

    result = call(client, '/register', 'POST', body)

    assert cookie is not None
    assert result['code'] == 401
    assert result['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_create_account_fail_not_admin(client):
    valid_credentials = base64.b64encode(b"sova@email.com:sova123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "employee_id": "123456",
        "name": "test",
        "phone_number": "12345678",
        "email": "test@test.com",
        "password": "test123"
    }

    result = call(client, '/register', 'POST', body)

    assert cookie is not None
    assert result['code'] == 403
    assert result['json']['message'] == "You not admin. Get out"


@pytest.mark.dependency()
def test_create_account_fail_exist_acc(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "employee_id": "000002",
        "name": "Jane Doe",
        "phone_number": "88888888",
        "email": "jane.doe@email.com",
        "password": "test123"
    }

    result = call(client, '/register', 'POST', body)

    assert cookie is not None
    assert result['code'] == 401
    assert result['json']['message'] == "Account already exist"


@pytest.mark.dependency()
def test_create_account_success(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    body = {
        "employee_id": "123456",
        "name": "test",
        "phone_number": "12345678",
        "email": "test@test.com",
        "password": "test123"
    }

    result = call(client, '/register', 'POST', body)
    
    body['role'] = 'user'
    body.pop('password')
    
    assert cookie is not None
    assert result['code'] == 201
    assert result['json']['message'] == body

# PROFILE

@pytest.mark.dependency()
def test_profile_fail_not_login(client):
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/myaccount')

    assert cookie is None
    assert result['code'] == 404
    assert result['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_profile_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token('john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/myaccount')

    assert cookie is not None
    assert result['code'] == 401
    assert result['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_profile_success(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/myaccount')

    assert cookie is not None
    assert result['code'] == 200

# GET ALL

@pytest.mark.dependency()
def test_get_all_fail_not_login(client):
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts')

    assert cookie is None
    assert result['code'] == 404
    assert result['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_all_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token('john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts')

    assert cookie is not None
    assert result['code'] == 401
    assert result['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_all_fail_not_admin(client):
    valid_credentials = base64.b64encode(b"sova@email.com:sova123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts')

    assert cookie is not None
    assert result['code'] == 403
    assert result['json']['message'] == "You not admin. Get out"


@pytest.mark.dependency()
def test_get_all_success(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts')

    assert cookie is not None
    assert result['code'] == 200

# GET ONE

@pytest.mark.dependency()
def test_get_one_fail_not_login(client):
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/1')

    assert cookie is None
    assert result['code'] == 404
    assert result['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_one_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token('john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/1')

    assert cookie is not None
    assert result['code'] == 401
    assert result['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_one_fail_not_admin(client):
    valid_credentials = base64.b64encode(b"sova@email.com:sova123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/1')

    assert cookie is not None
    assert result['code'] == 403
    assert result['json']['message'] == "You not admin. Get out"


@pytest.mark.dependency()
def test_get_one_fail_no_account(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/9999')

    assert cookie is not None
    assert result['code'] == 404
    assert result['json']['message'] == "There is no such account."


@pytest.mark.dependency()
def test_get_one_success(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/1')

    assert cookie is not None
    assert result['code'] == 200

# GET OWN

@pytest.mark.dependency()
def test_get_own_fail_not_login(client):
    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/0')

    assert cookie is None
    assert result['code'] == 404
    assert result['json']['message'] == "Not logged in"


@pytest.mark.dependency()
def test_get_own_fail_invalid_jwt(client):
    invalid_jwt = get_invalid_token('john.doe@email.com', 'test123', 'admin', '000001', 'John Doe')
    client.set_cookie('localhost', 'user-token', invalid_jwt)

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/0')

    assert cookie is not None
    assert result['code'] == 401
    assert result['json']['message'] == "Invalid JWT"


@pytest.mark.dependency()
def test_get_own_success(client):
    valid_credentials = base64.b64encode(b"john.doe@email.com:test123").decode("utf-8")
    client.get(
        "/login",
        headers={
            "Authorization": "Basic " + valid_credentials
    })

    cookie = next(
        (cookie for cookie in client.cookie_jar if cookie.name == "user-token"),
        None
    )

    result = call(client, '/accounts/0')

    assert cookie is not None
    assert result['code'] == 200