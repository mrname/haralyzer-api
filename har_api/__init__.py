from flask import Flask
from flask.ext.restful import Api
from har_api.models import db
from har_api.routes import create_routes


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object('har_api.settings')

    create_routes(api)

    db.init_app(app)
    return app
