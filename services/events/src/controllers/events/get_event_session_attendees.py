import os
import jwt

from flask import request, jsonify

from models import *


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

    session_attendees = Session_Attendee.query.filter_by(
        event_id = event_id
    ).all()
    
    if len(session_attendees) == 0:
        return jsonify(
            message="There are no participants enrolled in this event."
        ), 404

    result_list = []
    for session_attendee in session_attendees:
        dict = session_attendee.to_dict()
        result_list.append(dict['employee_id'])
    
    result_list = list(set(result_list))

    return jsonify(
        data={
            "participants": result_list
        }
    ), 200