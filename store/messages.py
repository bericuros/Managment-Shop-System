
from flask import jsonify

MESSAGE_AUTHORIZATION_HEADER = "Missing Authorization Header"
MESSAGE_FIELD_IS_MISSING = "Field {} is missing."
MESSAGE_INCORRECT_NUMBER_VALUES = "Incorrect number of values on line {}."
MESSAGE_INCORRECT_QUANTITY = "Incorrect quantity on line {}."
MESSAGE_INCORRECT_PRICE = "Incorrect price on line {}."
MESSAGE_PRODUCT_ID_MISSING_REQUEST = "Product id is missing for request number {}."
MESSAGE_PRODUCT_QUANTITY_MISSING_REQUEST = "Product quantity is missing for request number {}."
MESSAGE_INVALID_PRODUCT_ID_REQUEST = "Invalid product id for request number {}."
MESSAGE_INVALID_PRODUCT_QUANTITY_REQUEST = "Invalid product quantity for request number {}."
MESSAGE_INVALID_PRODUCT_REQUEST = "Invalid product for request number {}."


def getMessage(message, argument=None):
    if argument:
        return message.format(argument)
    return message


def responseMessageJson(message, argument=None, status=400):
    return jsonify(message=getMessage(message, argument)), status


def responseAuthorizationHeader(message, status=401):
    return jsonify(msg=message), status
