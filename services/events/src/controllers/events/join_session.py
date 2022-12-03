import os
import jwt

from flask import request, jsonify
from models import *

def controller(event_id, session_id):
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

    session = Session.query.filter_by(
        event_id=event_id,
        session_id=session_id
    ).first()

    if session == None:
        return jsonify(
            message="No such session"
        ), 401

    session_dict = session.to_dict()

    if session_dict['fill'] >= session_dict['capacity']:
        return jsonify(
            message="Unable to join session. (No more slots)"
        ), 401

    try:
        data = request.get_json(force=True)

        session_attendee = {}
        session_attendee['session_id'] = session_id
        session_attendee['event_id'] = event_id
        session_attendee['employee_id'] = token['employee_id']
        session_attendee['point'] = data['point']

        session_attendee = Session_Attendee(**session_attendee)
        db.session.add(session_attendee)

        updated_fill = session_dict['fill'] + 1
        setattr(session, "fill", updated_fill)

        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating session attendee.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "session_attendees": session_attendee.to_dict()
        }
    ), 201