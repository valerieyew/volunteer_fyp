from flask import Blueprint
from flask_cors import CORS, cross_origin

from controllers.community import get_event_posts, post_event_post

routes = Blueprint("community", __name__)
CORS(routes, supports_credentials=True)


@routes.route("/posts/<int:event_id>", methods=["GET"])
def route_get_all_posts(event_id):
    return get_event_posts.controller(event_id)

@routes.route("/posts/<int:event_id>", methods=["POST"])
def route_post_event_post(event_id):
    return post_event_post.controller(event_id)
