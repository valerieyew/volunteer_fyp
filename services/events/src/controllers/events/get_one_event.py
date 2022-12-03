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
        event_id = event_id
    ).first()

    if event == None:
        return jsonify(
            message="No such event"
        ), 401
        
    event_dict = event.to_dict()

    images = Image.query.filter_by(
        event_id = event_id
    ).all()

    images_to_add = []
    for image in images:
        image_to_add = image.to_dict()
        images_to_add.append(image_to_add['image'])
    event_dict["image_url"] = images_to_add

    tags = Tag.query.filter_by(
        event_id = event_id
    ).all()
    
    tags_to_add = []
    for tag in tags:
        tag_to_add = tag.to_dict()
        tags_to_add.append(tag_to_add['tag'])
    event_dict["tags"] = tags_to_add

    sessions = Session.query.filter_by(
        event_id = event_id
    ).all()

    session_list = []
    for session in sessions:
        session = session.to_dict()

        session_attendees = Session_Attendee.query.filter_by(
            event_id = event_id,
            session_id = session['session_id']
        ).all()

        attendees = []
        for session_attendee in session_attendees:
            session_attendee = session_attendee.to_dict()
            attendees.append(session_attendee)

        session['attendees'] = attendees
        session_list.append(session)

    return jsonify(
        {
            "event": event_dict,
            "sessions": session_list
        }
    ), 200
