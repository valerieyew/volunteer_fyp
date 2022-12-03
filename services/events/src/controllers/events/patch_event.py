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

    data = request.get_json(force=True)

    for key in data:
        setattr(event, key, data[key])

        if key == "image_url":
            # Delete existing images
            images_to_delete = Image.query.filter_by(
                event_id=event_id
            ).all()

            for image_to_delete in images_to_delete:
                db.session.delete(image_to_delete)

            # Add images to be updated
            for image_to_add in data[key]:
                image = {}
                image['event_id'] = event_id
                image['image'] = image_to_add
                image = Image(**image)
                db.session.add(image)

        if key == "tags":
            # Delete existing tags
            tags_to_delete = Tag.query.filter_by(
                event_id=event_id
            ).all()

            for tag_to_delete in tags_to_delete:
                db.session.delete(tag_to_delete)

            # Add tags to be updated
            for tag_to_add in data[key]:
                tag = {}
                tag['event_id'] = event_id
                tag['tag'] = tag_to_add
                tag = Tag(**tag)
                db.session.add(tag)
        
        if key == "sessions":

            sessions_to_delete = Session.query.filter_by(
                event_id=event_id
            ).all()

            # Delete all session attendees in sessions to be deleted
            for session_to_delete in sessions_to_delete:
                session_to_delete_dict = session_to_delete.to_dict()

                session_attendees_to_delete = Session_Attendee.query.filter_by(
                    event_id=event_id,
                    session_id = session_to_delete_dict['session_id']
                ).all()

                for session_attendee_to_delete in session_attendees_to_delete:
                    db.session.delete(session_attendee_to_delete)

            # Then delete respective sessions
            for session_to_delete in sessions_to_delete:
                db.session.delete(session_to_delete)

            last_session = Session.query.order_by(Session.session_id.desc()).first()
            new_session_id = last_session.session_id + 1

            # Add the sessions to be updated
            for session_to_add in data['sessions']:
                session = {}
                session['session_id'] = new_session_id
                new_session_id += 1
                session['event_id'] = event_id
                session['start_time'] = session_to_add['start_time']
                session['end_time'] = session_to_add['end_time']
                session['capacity'] = session_to_add['capacity']
                session['fill'] = session_to_add['fill']
                session = Session(**session)
                db.session.add(session)

    setattr(event, "status", "Pending")
    setattr(event, "comments", "")
    setattr(event, "last_admin_action_by", "")
    db.session.commit()

    return jsonify(
        {
            "event": event.to_dict()
        }
    ), 200