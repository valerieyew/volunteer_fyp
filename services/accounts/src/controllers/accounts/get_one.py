import os
import jwt

from flask import request, jsonify

from models import db, Account


def controller(employee_id):
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

    if (account_match.role != "admin"):
        return jsonify(
            message="You not admin. Get out"
        ), 403

    account = Account.query.filter_by(employee_id=employee_id).first()

    if account is not None:
        return jsonify(
            {
                "data": {
                    "account": account.to_dict()
                }
            }
        ), 200
    return jsonify(
        {
            "message": "There is no such account."
        }
    ), 404
