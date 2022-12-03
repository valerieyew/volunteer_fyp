import os
import jwt

from flask import request, jsonify

from models import Session_Attendee, Session, Event, Image

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
    
    session_attendee_list = Session_Attendee.query.filter_by(
        employee_id = token['employee_id']
    ).all()

    if len(session_attendee_list) == 0:
        return jsonify(
            message="No events attended."
        ), 404

    res = {
        "enrolled": []
    }

    for session_attendees in session_attendee_list:
        session_attendee = session_attendees.to_dict()
        session_to_add = session_attendee["session_id"]
        event_to_add = session_attendee["event_id"]

        event = Event.query.filter_by(
            event_id = event_to_add
        ).first().to_dict()

        images = Image.query.filter_by(
            event_id=event["event_id"]
        ).all()

        images_to_add = []
        for image in images:
            image_to_add = image.to_dict()
            images_to_add.append(image_to_add['image'])
        event["image_url"] = images_to_add

        session = Session.query.filter_by(
            session_id = session_to_add
        ).first()
        
        event["sessions"] = session.to_dict()
        
        res["enrolled"].append(event)

    return jsonify(res), 200