from flask import Blueprint
from flask_cors import CORS, cross_origin

from controllers.events import *

routes = Blueprint("events", __name__)
CORS(routes, supports_credentials=True)


@routes.route("/events", methods=["GET"])
def route_get_all_approved():
    return get_all_approved.controller()


@routes.route("/events/pending", methods=["GET"])
def route_get_all_pending():
    return get_all_pending.controller()


@routes.route("/events/rejected", methods=["GET"])
def route_get_all_rejected():
    return get_all_rejected.controller()


@routes.route("/events/proposed", methods=["GET"])
def route_get_all_proposed():
    return get_all_proposed.controller()


@routes.route("/events/enrolled", methods=["GET"])
def route_get_all_enrolled():
    return get_all_enrolled.controller()


@routes.route("/events/<int:event_id>", methods=["GET"])
def route_get_one_event(event_id):
    return get_one_event.controller(event_id)


@routes.route("/events/<int:event_id>/approve", methods=["PATCH"])
def route_approve_event(event_id):
    return approve_event.controller(event_id)


@routes.route("/events/<int:event_id>/reject", methods=["PATCH"])
def route_reject_event(event_id):
    return reject_event.controller(event_id)


@routes.route("/events", methods=["POST"])
def route_create_event():
    return create_event.controller()


@routes.route("/events/<int:event_id>/sessions", methods=["POST"])
def route_create_session(event_id):
    return create_session.controller(event_id)


@routes.route("/events/<int:event_id>/<int:session_id>", methods=["POST"])
def route_join_session(event_id, session_id):
    return join_session.controller(event_id, session_id)


@routes.route("/events/<int:event_id>", methods=["PATCH"])
def route_patch_event(event_id):
    return patch_event.controller(event_id)


@routes.route("/events/<int:event_id>/participants", methods=["GET"])
def route_get_event_session_attendees(event_id):
    return get_event_session_attendees.controller(event_id)


@routes.route("/events/<int:event_id>/attendances", methods=["GET"])
def route_get_user_attendances(event_id):
    return get_user_attendances.controller(event_id)


@routes.route("/events/<tag>", methods=["GET"])
def route_get_events_tag(tag):
    return get_events_tag.controller(tag)
