from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, User, UserRole
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required,\
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_

application = Flask(__name__)
application.config.from_object(Configuration)


@application.route("/", methods=["GET"])
def index():
    return Response("Hello world!", status=200)


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, port=5002)
