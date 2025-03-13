from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .home.routes import home


from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(home, url_prefix='/')

    db.init_app(app)

    return app
