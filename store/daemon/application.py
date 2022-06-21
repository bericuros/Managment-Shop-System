from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, Product, ProductOrder, ProductCategory, Order, Category
from redis import Redis
from sqlalchemy import and_

application = Flask(__name__)
application.config.from_object(Configuration)


def calculatePrice(currentPrice, currentQuantity, deliveryPrice, deliveryQuantity):
    return (currentPrice * currentQuantity + deliveryPrice * deliveryQuantity) / (currentQuantity + deliveryQuantity)


if __name__ == "__main__":
    database.init_app(application)

    while True:
        with application.app_context() as context:
            with Redis(Configuration.REDIS_HOST) as redis:
                print("Waiting...")

                redisCategories = redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8")
                redisName = redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8")
                redisQuantity = int(redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8"))
                redisPrice = float(redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8"))

                print(f"Read: ({redisCategories}, {redisName}, {redisQuantity}, {redisPrice})")

                categories = redisCategories.split("|")
                product = Product.query.filter(Product.name == redisName).first()
                if product:
                    productCategories = product.categories
                    productNameCategories = []
                    for elem in productCategories:
                        productNameCategories.append(elem.name)

                    productNameCategories.sort()
                    categories.sort()

                    if categories == productNameCategories:
                        product.price = calculatePrice(product.price, product.quantity, redisPrice, redisQuantity)
                        product.quantity += redisQuantity
                        database.session.commit()
                else:
                    product = Product(name=redisName, quantity=redisQuantity, price=redisPrice)
                    database.session.add(product)
                    database.session.commit()
                    for category in categories:
                        queryCategory = Category.query.filter(Category.name == category).first()
                        if not queryCategory:
                            queryCategory = Category(name=category)
                            database.session.add(queryCategory)
                            database.session.commit()
                        productCategory = ProductCategory(productId=product.id, categoryId=queryCategory.id)
                        database.session.add(productCategory)
                        database.session.commit()

                productOrders = ProductOrder.query.filter(
                    and_(
                        ProductOrder.productId == product.id,
                        ProductOrder.requested != ProductOrder.received
                    )
                ).order_by(ProductOrder.orderId).all()
                for productOrder in productOrders:
                    needs = productOrder.requested - productOrder.received
                    productOrder.received += min(needs, product.quantity)
                    product.quantity = max(product.quantity - needs, 0)
                    if product.quantity == 0:
                        break
                database.session.commit()
