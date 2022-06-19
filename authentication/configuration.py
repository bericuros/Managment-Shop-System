
from datetime import timedelta;


class Configuration:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/authentication"
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
