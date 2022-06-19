
from flask import jsonify

MESSAGE_FIELD_IS_MISSING = "Field {} is missing."
MESSAGE_INVALID_EMAIL = "Invalid email."
MESSAGE_INVALID_PASSWORD = "Invalid password."
MESSAGE_EMAIL_ALREADY_EXISTS = "Email already exists."
MESSAGE_INVALID_CREDENTIALS = "Invalid credentials."
MESSAGE_UNKNOWN_USER = "Unknown user."


def getMessage(message, argument=None):
    if argument:
        return message.format(argument)
    return message


def responseMessageJson(message, argument=None, status=400):
    return jsonify(message=getMessage(message, argument)), status
