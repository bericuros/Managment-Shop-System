from flask import Flask, request, Response, jsonify
from configurationRedis import Configuration
from models import database
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_
from messages import *
import io
import csv
from redis import Redis
from check import role_check
import re

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


def isQuantityValid(quantity):
    return re.search(r"^[1-9]+[0-9]*$", quantity)


def isPriceValid(price):
    return re.search(r"^[0-9]+[.]?[0-9]*$", price)


@application.route("/", methods=["GET"])
def index():
    return "hi"


@application.route("/update", methods=["POST"])
@jwt_required(refresh=False)
@role_check(role="warehouse")
def update():
    keys = request.files.keys()
    if not ("file" in keys):
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "file")

    file = request.files["file"]
    if not file:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "file")

    content = file.stream.read().decode("utf-8")
    stream = io.StringIO(content)
    reader = csv.reader(stream)

    rows = []
    for row in reader:
        rows.append(row)

    for i in range(len(rows)):
        if len(rows[i]) != 4:
            return responseMessageJson(MESSAGE_INCORRECT_NUMBER_VALUES, str(i))

    for i in range(len(rows)):
        if not isQuantityValid(rows[i][2]) or int(rows[i][2]) <= 0:
            return responseMessageJson(MESSAGE_INCORRECT_QUANTITY, str(i))

    for i in range(len(rows)):
        if not isPriceValid(rows[i][3]) or float(rows[i][3]) <= 0:
            return responseMessageJson(MESSAGE_INCORRECT_PRICE, str(i))

    with Redis(Configuration.REDIS_HOST) as redis:
        for row in rows:
            redis.rpush(Configuration.REDIS_PRODUCTS, *row)

    return Response(status=200)


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5006)
