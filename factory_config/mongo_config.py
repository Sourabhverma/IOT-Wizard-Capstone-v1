from flask_pymongo import PyMongo
from flask import Flask

mongo = PyMongo()


class IotDatabase:
    def create_app(config):
        app = Flask(__name__, instance_relative_config=False)
        app.config.from_object(config)
        mongo.init_app(app)
        return app
