from flask import Blueprint
from flask_cors import CORS

from controllers.authentication import create_account, login, logout, profile

routes = Blueprint("authentication", __name__)
CORS(routes, supports_credentials=True)


@routes.route("/register", methods=["POST"])
def route_create_account():
    return create_account.controller()


@routes.route("/login") #, methods=["POST"]
def route_login():
    return login.controller()


@routes.route("/logout", methods=["POST"])
def route_logout():
    return logout.controller()


@routes.route("/myaccount", methods=["GET"])
def route_profile():
    return profile.controller()
