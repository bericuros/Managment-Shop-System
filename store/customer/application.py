from flask import Flask, request, Response, jsonify
from store.configuration import Configuration
from store.models import database, Order, ProductOrder, Product, ProductCategory, Category
from email.utils import parseaddr
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    create_refresh_token, get_jwt, get_jwt_identity
from sqlalchemy import and_

application = Flask(__name__)
application.config.from_object(Configuration)
jwt = JWTManager(application)


@application.route("/", methods=["GET"])
def index():
    return "hi"


@application.route("/search", methods=["GET"])
def search():
    name = request.args.get("name", "")
    category = request.args.get("category", "")

    categories = Category.query.filter(Category.name.like(f"%{category}%")).all()
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
def order():
    return "TODO"


@application.route("/status", methods=["GET"])
def status():
    return "TODO"


if __name__ == "__main__":
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5004)
