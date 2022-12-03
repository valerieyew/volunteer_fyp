import os
import jwt

from models import Account

from flask import request, jsonify


def controller():
    encrypted_token = request.cookies.get('user-token')
    if (not encrypted_token):
        return jsonify(
            message="Not logged in"
        ), 404

    try:
        token = jwt.decode(
            encrypted_token,
            os.environ.get("COOKIE_JWT_SECRET"),
            algorithms=["HS256"]
        )
    except jwt.exceptions.InvalidSignatureError:
        return jsonify(
            message="Invalid JWT"
        ), 401

    account_match = Account.query.filter_by(
        email=token["email"],
        password=token["password"],
    ).first()

    if (account_match is None):
        return jsonify(
            message="Invalid email or password."
        ), 404

    return jsonify(
        message=account_match.to_dict()
    ), 200
