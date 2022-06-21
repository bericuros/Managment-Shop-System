
import os

databaseUrl = os.environ["DATABASE_URL"]


class Configuration:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:root@{databaseUrl}/store"
    REDIS_HOST = "localhost"
    REDIS_PRODUCTS = "products"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"




