from flask import Flask
from flask_restful import Api
from har_api.models import db


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config.from_object('har_api.settings')

    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
