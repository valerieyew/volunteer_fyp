from flask import jsonify


def controller():
    return jsonify(
        message="Welcome to CS480 FYP by Team Vision (community)"
    ), 200
