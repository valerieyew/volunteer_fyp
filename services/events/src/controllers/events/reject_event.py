import os
import jwt

from flask import request, jsonify
import sqlalchemy
from models import db, Event

def controller(event_id):
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

    if token["role"] != "admin":
        return jsonify(
            message="You not admin. Get out"
        ), 403
    
    event = Event.query.filter_by(
        event_id = event_id
    ).first()

    setattr(event, "status", "Rejected")
    setattr(event, "last_admin_action_by", token['email'])

    try:
        data = request.get_json(force=True)
        setattr(event, "comments", data['comments'])
    except Exception as e:
        return jsonify(
            {
                "message": "No comments field in request body.",
                "error": str(e)
            }
        ), 500
        
    try:
        db.session.commit()
    except (sqlalchemy.exc.IntegrityError, sqlalchemy.exc.InvalidRequestError):
        return jsonify(
            message="DB error"
        ), 401

    return jsonify(
        event.to_dict()
    ), 201