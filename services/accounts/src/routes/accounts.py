from flask import Blueprint
from flask_cors import CORS

from controllers.accounts import get_all, get_one, get_own

routes = Blueprint("accounts", __name__)
CORS(routes, supports_credentials=True)

@routes.route("/accounts", methods=["GET"])
def route_get_all():
    return get_all.controller()

@routes.route("/accounts/<int:employee_id>", methods=["GET"])
def route_get_one(employee_id):
    return get_one.controller(employee_id)

@routes.route("/accounts/0", methods=["GET"])
def route_get_own():
    return get_own.controller()