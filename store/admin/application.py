from flask import Flask, request, Response, jsonify
from store.configuration import Configuration
from store.models import database, Product, ProductOrder, ProductCategory, Order, Category
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_
from store.messages import *
from check import role_check

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


@application.route("/", methods=["GET"])
def index():
    return "hi"


@application.route("/productStatistics", methods=["GET"])
@jwt_required(refresh=False)
@role_check(role="admin")
def productStatistics():
    statistics = []
    products = Product.query.all()
    for product in products:
        data = {"name": product.name, "sold": 0, "waiting": 0}
        productOrders = ProductOrder.query.filter(ProductOrder.productId == product.id)
        for productOrder in productOrders:
            data["sold"] += productOrder.received
            data["waiting"] += productOrder.requested - productOrder.received
        if data["sold"]:
            statistics.append(data)
    return jsonify(statistics=statistics), 200


@application.route("/categoryStatistics", methods=["GET"])
@jwt_required(refresh=False)
@role_check(role="admin")
def categoryStatistics():
    return "TODO"


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5003)
