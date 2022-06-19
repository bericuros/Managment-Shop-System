
from flask import jsonify

MESSAGE_FIELD_IS_MISSING = "Field {} is missing."
MESSAGE_INVALID_EMAIL = "Invalid email."
MESSAGE_INVALID_PASSWORD = "Invalid password."
MESSAGE_EMAIL_ALREADY_EXISTS = "Email already exists."
MESSAGE_INVALID_CREDENTIALS = "Invalid credentials."


def messageJson(message, argument=None):
    if argument:
        return {"message": message.format(argument)}
    return {"message": message}


def responseMessageJson(message, argument=None, status=400):
    return jsonify(messageJson(message, argument)), status
