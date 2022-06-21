from flask import Flask
from configurationDatabase import Configuration
from flask_migrate import Migrate, init, migrate, upgrade
from models import database
from sqlalchemy_utils import database_exists, create_database

application = Flask(__name__)
application.config.from_object(Configuration)

migrateObject = Migrate(application, database)

if not database_exists(Configuration.SQLALCHEMY_DATABASE_URI):
    create_database(Configuration.SQLALCHEMY_DATABASE_URI)

database.init_app(application)

with application.app_context() as context:
    try:
        init()
    except:
        dummy = 0
    try:
        migrate(message="Initial migration.")
    except:
        dummy = 0
    try:
        upgrade()
    except:
        dummy = 0
