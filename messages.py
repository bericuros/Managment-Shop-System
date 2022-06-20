
from flask import jsonify

MESSAGE_AUTHORIZATION_HEADER = "Missing Authorization Header"


def getMessage(message, argument=None):
    if argument:
        return message.format(argument)
    return message


def responseMessageJson(message, argument=None, status=400):
    return jsonify(message=getMessage(message, argument)), status


def responseAuthorizationHeader(message, status=401):
    return jsonify(msg=message), status
