import datetime

from flask import Flask, request, Response, jsonify
from store.configuration import Configuration
from store.models import database, Order, ProductOrder, Product, ProductCategory, Category
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_
from messages import *
from check import role_check
import re

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


def isQuantityValid(quantity):
    return re.search(r"^[1-9]+[0-9]*$", quantity)


@application.route("/", methods=["GET"])
def index():
    return "hi"


@application.route("/search", methods=["GET"])
@jwt_required(refresh=False)
@role_check(role="customer")
def search():
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    categories = Category.query.join(ProductCategory).join(Product).filter(
        and_(
            Product.name.like(f"%{name}%"),
            Category.name.like(f"%{category}%"),
        )
    ).all()
    products = Product.query.join(ProductCategory).join(Category).filter(
        and_(
            Product.name.like(f"%{name}%"),
            Category.name.like(f"%{category}%"),
        )
    ).all()

    jsonCategories = []
    for elem in categories:
        jsonCategories.append(elem.name)
    jsonCategories.sort()

    jsonProducts = []
    for product in products:
        data = {"categories": [elem.name for elem in product.categories], "id": product.id, "name": product.name,
                "price": product.price, "quantity": product.quantity}
        jsonProducts.append(data)

    return jsonify(categories=jsonCategories, products=jsonProducts), 200


@application.route("/order", methods=["POST"])
@jwt_required(refresh=False)
@role_check(role="customer")
def order():
    requests = request.json.get("requests", None)
    if not requests:
        return responseMessageJson(MESSAGE_FIELD_IS_MISSING, "requests")

    for i in range(len(requests)):
        id = requests[i].get("id", None)
        if not id:
            return responseMessageJson(MESSAGE_PRODUCT_ID_MISSING_REQUEST, str(i))

    for i in range(len(requests)):
        quantity = requests[i].get("quantity", None)
        if not quantity:
            return responseMessageJson(MESSAGE_PRODUCT_QUANTITY_MISSING_REQUEST, str(i))

    for i in range(len(requests)):
        id = requests[i].get("id", 0)
        if not isQuantityValid(str(id)) or id <= 0:
            return responseMessageJson(MESSAGE_INVALID_PRODUCT_ID_REQUEST, str(i))

    for i in range(len(requests)):
        quantity = requests[i].get("quantity", 0)
        if not isQuantityValid(str(quantity)) or quantity <= 0:
            return responseMessageJson(MESSAGE_INVALID_PRODUCT_QUANTITY_REQUEST, str(i))

    for i in range(len(requests)):
        id = requests[i].get("id")
        product = Product.query.filter(Product.id == id).first()
        if not product:
            return responseMessageJson(MESSAGE_INVALID_PRODUCT_REQUEST, str(i))

    order = Order(identity=get_jwt_identity(), price=0, timestamp=datetime.datetime.utcnow())
    database.session.add(order)
    database.session.commit()

    productIdSet = {int(requests[i].get("id")) for i in range(len(requests))}
    productDict = {}
    for productId in productIdSet:
        productDict[productId] = 0
    for i in range(len(requests)):
        productDict[int(requests[i].get("id"))] += int(requests[i].get("quantity"))
    for id in productDict:
        product = Product.query.filter(Product.id == id).first()
        order.price += product.price * productDict[id]
        productOrder = ProductOrder(productId=product.id, orderId=order.id,
                                    requested=productDict[id], received=min(productDict[id], product.quantity),
                                    price=product.price)
        product.quantity = max(product.quantity - productDict[id], 0)
        database.session.add(productOrder)
        database.session.commit()

    return jsonify(id=order.id), 200


@application.route("/status", methods=["GET"])
@jwt_required(refresh=False)
@role_check(role="customer")
def status():
    identity = get_jwt_identity()
    orders = Order.query.filter(Order.identity == identity).all()

    jsonOrders = []
    for order in orders:
        productOrders = ProductOrder.query.filter(ProductOrder.orderId == order.id).all()
        jsonProducts = []
        notReceivedCount = 0
        for productOrder in productOrders:
            product = Product.query.filter(Product.id == productOrder.productId).first()
            data = {"categories": [elem.name for elem in product.categories], "name": product.name,
                    "price": productOrder.price, "received": productOrder.received,
                    "requested": productOrder.requested}
            jsonProducts.append(data)
            notReceivedCount += productOrder.requested - productOrder.received
        status = "PENDING" if notReceivedCount else "COMPLETE"
        data = {"products": jsonProducts, "price": order.price, "status": status,
                "timestamp": order.timestamp.replace(microsecond=0).isoformat() + "Z"}
        jsonOrders.append(data)

    return jsonify(orders=jsonOrders), 200


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5004)
