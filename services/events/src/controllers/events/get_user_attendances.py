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

    attendances = Session_Attendee.query.filter_by(
        event_id = event_id,
        employee_id = token['employee_id']
    ).all()

    if len(attendances) == 0:
        return jsonify(
            message="Did not participate in this event."
        ), 404

    result_list = []
    for attendance in attendances:
        dict = attendance.to_dict()
        result_list.append(dict)

    return jsonify(
        data={
            "attendance": result_list
        }
    ), 200