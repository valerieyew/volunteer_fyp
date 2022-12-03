from flask import Blueprint
from flask_cors import CORS

from controllers.root import base

routes = Blueprint("root", __name__)
CORS(routes)

routes.route("/", methods=["GET"])(base.controller)