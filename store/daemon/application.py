from flask import Flask, request, Response, jsonify
from store.configuration import Configuration
from store.models import database, Product, ProductOrder, ProductCategory, Order, Category
from redis import Redis

application = Flask(__name__)
application.config.from_object(Configuration)


if __name__ == "__main__":
    database.init_app(application)

    with application.app_context() as context:
        while True:
            with Redis(Configuration.REDIS_HOST) as redis:
                print("Waiting...")
                categories = redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8")
                name = redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8")
                quantity = redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8")
                price = redis.blpop(Configuration.REDIS_PRODUCTS)[1].decode("utf-8")
                print(f"Read: {categories},{name},{quantity},{price}")

                




    # application.run(debug=True, host="0.0.0.0", port=5005)
