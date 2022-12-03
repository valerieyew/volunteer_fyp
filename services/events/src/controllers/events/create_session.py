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

    event = Event.query.filter_by(
        event_id=event_id
    ).first()

    if event == None:
        return jsonify(
            message="No such event"
        ), 401

    event_dict = event.to_dict()

    if event_dict['employee_id'] != token['employee_id']:
        return jsonify(
            message="Wrong employee_id"
        ), 401

    try:
        data = request.get_json(force=True)

        session = {}
        last_session = Session.query.order_by(
            Session.session_id.desc()).first()
        new_session_id = last_session.session_id + 1
        session['session_id'] = new_session_id
        session['event_id'] = event_id
        session['start_time'] = data['start_time']
        session['end_time'] = data['end_time']
        session['capacity'] = data['capacity']
        session['fill'] = 0

        session = Session(**session)
        db.session.add(session)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating session.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "event": session.to_dict()
        }
    ), 201
