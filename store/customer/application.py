from flask import Flask, request, Response, jsonify
from store.configuration import Configuration
from store.models import database
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


@application.route("/", methods=["GET"])
def index():
    return "hi"


@application.route("/search", methods=["GET"])
def search():
    return "TODO"


@application.route("/order", methods=["POST"])
def order():
    return "TODO"


@application.route("/status", methods=["GET"])
def status():
    return "TODO"


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5004)
