import os
import jwt

from models import db, Account

import sqlalchemy
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

    if (account_match.role != "admin"):
        return jsonify(
            message="You not admin. Get out"
        ), 403

    data = request.get_json()

    employee_id = data["employee_id"]
    name = data["name"]
    phone_number = data["phone_number"]
    email = data["email"]
    password = data["password"]

    new_account = Account(
        employee_id,
        name,
        phone_number,
        email,
        password,
        "user",
    )

    account_json = new_account.to_dict()

    try:
        db.session.add(new_account)
        db.session.commit()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
        return jsonify(
            message="Account already exist"
        ), 401

    return jsonify(
        message=account_json
    ), 201
