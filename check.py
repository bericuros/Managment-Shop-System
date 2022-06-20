from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import Response
from messages import *


def role_check(role):
    def inner_role(function):
        @wraps(function)
        def decorator(*arguments, **keyword_arguments):
            verify_jwt_in_request()
            claims = get_jwt()
            if ("roles" in claims) and (role in claims["roles"]):
                return function(*arguments, **keyword_arguments)
            else:
                return responseAuthorizationHeader(MESSAGE_AUTHORIZATION_HEADER)
        return decorator
    return inner_role
