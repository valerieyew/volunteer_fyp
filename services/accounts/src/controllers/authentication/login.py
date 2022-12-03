import os
import jwt
from hashlib import sha1

from models import Account

from flask import request, make_response, jsonify


def controller():
    res = make_response("Setting a cookie")

    auth = request.authorization

    email = auth.username
    password = auth.password
    password_hashed = sha1(password.encode('utf-8')).hexdigest()

    account_match = Account.query.filter_by(
        email=email,
        password=password_hashed
    ).first()

    if (account_match is None):
        return jsonify(
            message="Account doesn't exist"
        ), 404

    res = jsonify(message=account_match.to_dict())

    encrypted_token = jwt.encode(
        {
            "email": email,
            "password": password_hashed,
            "role": account_match.role,
            "employee_id": account_match.employee_id,
            "name": account_match.name
        },
        os.environ.get("COOKIE_JWT_SECRET"),
        algorithm="HS256"
    )

    if os.environ.get("stage") == "production":
        res.set_cookie(
            'user-token',
            encrypted_token,
            path='/',
            httponly=True,
            secure=True,
            domain=".teamvision.link",
            max_age=(3600 * 24 * 30)
        )
        res.headers.add('Set-Cookie', 'cross-site-cookie=bar; SameSite=None; Secure')
    else:
        res.set_cookie(
            'user-token',
            encrypted_token,
            path='/',
            httponly=True,
            max_age=(3600 * 24 * 30)
        )

    return res, 200
