from flask import Flask
from flask_cors import CORS
from flask.ext.restful import Api
from har_api.models import db
from har_api.routes import create_routes


def create_app():
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    app.config.from_object('har_api.settings')
    app.config.from_envvar('APP_SETTINGS', silent=True)

    create_routes(api)

    db.init_app(app)
    return app
