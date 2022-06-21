
import os

databaseUrl = os.environ["DATABASE_URL"]
redisUrl = os.environ["REDIS_URL"]


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/store"
    REDIS_HOST = redisUrl
    REDIS_PRODUCTS = "products"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"




