from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, User, UserRole, Role
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_
from messages import *
import re

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


@application.route("/", methods=["GET"])
def index():
    return Response("Hello world!", status=200)


@application.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")
    isCustomer = request.json.get("isCustomer", None)

    if len(email) == 0:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "email")
    if len(password) == 0:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "password")
    if len(forename) == 0:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "forename")
    if len(surname) == 0:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "surname")
    if isCustomer is None:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "isCustomer")

    if not re.search(r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z]{2,}$", email):
        return responseMessageJson(MESSAGE_INVALID_EMAIL)

    if len(password) < 8 or \
            not any([letter.isdigit() for letter in password]) or \
            not any([letter.isupper() for letter in password]) or \
            not any([letter.islower() for letter in password]):
        return responseMessageJson(MESSAGE_INVALID_PASSWORD)

    if User.query.filter(User.email == email).first():
        return responseMessageJson(MESSAGE_EMAIL_ALREADY_EXISTS)

    role = Role.query.filter(Role.name == ("customer" if isCustomer else "warehouse")).first()

    user = User(email=email, password=password, forename=forename, surname=surname)
    database.session.add(user)
    database.session.commit()

    userRole = UserRole(userId=user.id, roleId=role.id)
    database.session.add(userRole)
    database.session.commit()

    return Response("Successful registration.", status=200)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    if len(email) == 0:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "email")
    if len(password) == 0:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "password")

    if not re.search(r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z]{2,}$", email):
        return responseMessageJson(MESSAGE_INVALID_EMAIL)

    user = User.query.filter(
        and_(
            User.email == email,
            User.password == password,
        )
    ).first()

    if not user:
        return responseMessageJson(MESSAGE_INVALID_CREDENTIALS)

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": [str(role) for role in user.roles],
    }

    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)
    refreshToken = create_refresh_token(identity=user.email, additional_claims=additionalClaims)

    return jsonify(accessToken=accessToken, refreshToken=refreshToken), 200


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, port=5002)
