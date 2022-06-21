
import os

redisUrl = os.environ["REDIS_URL"]


class Configuration:
    REDIS_HOST = redisUrl
    REDIS_PRODUCTS = "products"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"




