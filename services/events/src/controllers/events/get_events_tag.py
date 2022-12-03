import os
import jwt

from flask import request, jsonify

from models import Event, Image, Tag


def controller(tag):
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

    tag_events = Tag.query.filter_by(
        tag=tag
    ).all()

    if len(tag_events) == 0:
        return jsonify(
            message="There are no events."
        ), 404
        
    tag_events_id = []
    for tag_event in tag_events:
        tag_event = tag_event.to_dict()
        tag_event_id = tag_event['event_id']
        tag_events_id.append(tag_event_id)

    result_list = []
    for id in tag_events_id:
        event_dict = Event.query.filter_by(
            event_id=id
        ).first().to_dict()

        images = Image.query.filter_by(
            event_id=id
        ).all()

        images_to_add = []
        for image in images:
            image_to_add = image.to_dict()
            images_to_add.append(image_to_add['image'])
        event_dict["image_url"] = images_to_add

        result_list.append(event_dict)

    return jsonify(
        data={
            "events": result_list
        }
    ), 200

