import os
import jwt

from flask import request, jsonify

from models import Event, Image


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

    event_list = Event.query.filter_by(
        status="Approved"
    ).all()

    if len(event_list) == 0:
        return jsonify(
            message="There are no events."
        ), 404

    result_list = []
    for event in event_list:
        dict = event.to_dict()

        images = Image.query.filter_by(
            event_id=dict["event_id"]
        ).all()
        
        images_to_add = []
        for image in images:
            image_to_add = image.to_dict()
            images_to_add.append(image_to_add['image'])
        dict["image_url"] = images_to_add
        
        result_list.append(dict)

    return jsonify(
        data={
            "events": result_list
        }
    ), 200
