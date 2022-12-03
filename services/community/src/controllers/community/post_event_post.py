from multiprocessing import Event
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

    event = db.session.execute('SELECT * FROM events WHERE event_id = :val', {'val': event_id}).first()

    if event == None:
        return jsonify(
            message="No such event"
        ), 401

    try:
        data = request.get_json(force=True)

        post = {}
        last_post = Post.query.order_by(
            Post.post_id.desc()).first()
        new_post_id = last_post.post_id + 1
        post['post_id'] = new_post_id
        post['post_title'] = data['post_title']
        post['post_message'] = data['post_message']
        post['event_id'] = event_id
        post['posted_by_id'] = token['employee_id']
        post['posted_by_name'] = token['name']
        
        post = Post(**post)
        db.session.add(post)
        db.session.commit()

    except Exception as e:
        return jsonify(
            {
                "message": "An error occurred creating post.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "post": post.to_dict()
        }
    ), 201