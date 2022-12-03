import os
import jwt

from flask import request, jsonify

from models import *


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

    try:
        data = request.get_json(force=True)

        if not all(key in data for key in ('name', 'location', 'proposal_details',
                                           'info', 'registration_opens_on',
                                           'registration_closes_on',
                                           'image_url', 'sessions', 'tags')):
            return jsonify(
                {
                    "message": "An error occurred creating event. (Lack of required keys in event)"
                }
            ), 404

        if 'sessions' in data:
            for session in data['sessions']:
                if not all(key in session for key in ('start_time', 'end_time', 'capacity', 'fill')):
                    return jsonify(
                        {
                            "message": "An error occurred creating event. (Lack of required keys in sessions)"
                        }
                    ), 404

        event = {}
        last_event = Event.query.order_by(Event.event_id.desc()).first()
        new_event_id = last_event.event_id + 1
        event['event_id'] = new_event_id
        event['employee_id'] = token['employee_id']
        event['name'] = data['name']
        event['location'] = data['location']
        event['proposal_details'] = data['proposal_details']
        event['info'] = data['info']
        event['registration_opens_on'] = data['registration_opens_on']
        event['registration_closes_on'] = data['registration_closes_on']
        event['status'] = 'Pending'
        event['comments'] = ''
        event['last_admin_action_by'] = ''

        event = Event(**event)
        db.session.add(event)
        db.session.commit()

        for image_to_add in data['image_url']:
            image = {}
            image['event_id'] = new_event_id
            image['image'] = image_to_add
            image = Image(**image)
            db.session.add(image)
            db.session.commit()

        last_session = Session.query.order_by(
            Session.session_id.desc()).first()
        new_session_id = last_session.session_id + 1
        for session_to_add in data['sessions']:
            session = {}
            session['session_id'] = new_session_id
            new_session_id += 1
            session['event_id'] = new_event_id
            session['start_time'] = session_to_add['start_time']
            session['end_time'] = session_to_add['end_time']
            session['capacity'] = session_to_add['capacity']
            session['fill'] = session_to_add['fill']
            session = Session(**session)
            db.session.add(session)
            db.session.commit()

        for tag_to_add in data['tags']:
            tag = {}
            tag['event_id'] = new_event_id
            tag['tag'] = tag_to_add
            tag = Tag(**tag)
            db.session.add(tag)
            db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating event.",
                "error": str(e)
            }
        ), 500
    return jsonify(
        {
            "event": event.to_dict()
        }
    ), 201
