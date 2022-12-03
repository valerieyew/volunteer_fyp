import os
import jwt

from flask import request, jsonify

from models import Post


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

    posts_list = Post.query.filter_by(
        event_id=event_id
    ).all()

    if len(posts_list) == 0:
        return jsonify(
            message="There are no posts."
        ), 404

    result_list = []
    for post in posts_list:
        dict = post.to_dict()
        result_list.append(dict)

    return jsonify(
        data={
            "posts": result_list
        }
    ), 200
