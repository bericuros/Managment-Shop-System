from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, Product, ProductOrder, ProductCategory, Order, Category
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_
from messages import *
from check import role_check
from sqlalchemy import func

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
            data["sold"] += productOrder.requested
            data["waiting"] += productOrder.requested - productOrder.received
        if data["sold"]:
            statistics.append(data)
    return jsonify(statistics=statistics), 200


@application.route("/categoryStatistics", methods=["GET"])
@jwt_required(refresh=False)
@role_check(role="admin")
def categoryStatistics():
    statistics = []
    count = func.sum(ProductOrder.requested)
    categories = Category.query.join(ProductCategory).join(Product).\
        outerjoin(ProductOrder).group_by(Category).with_entities(Category, count). \
        order_by(count.desc()).order_by(Category.name).all()
    for category in categories:
        statistics.append(category[0].name)
    return jsonify(statistics=statistics), 200


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5003)
