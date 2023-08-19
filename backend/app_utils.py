import os

from flask import Flask
from flask_cors import CORS

from config import Config


def create_app(name):
    app = Flask(name)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    load_app_params(app)

    # app.config.from_pyfile('config.py')
    app.config.from_object(Config)
    app.config.from_prefixed_env()

    # Initializing database connection
    from models import db
    db.init_app(app)

    # Initializing schema connection
    from backend.schema import ma
    ma.init_app(app)

    from apis import blueprint as apis_bp
    app.register_blueprint(apis_bp, url_prefix="/api")

    # from views import blueprint as views_bp
    # app.register_blueprint(views_bp, url_prefix="/")

    return app


def load_app_params(app: Flask, prefix: str = 'APP_PARAM_'):
    for key in sorted(os.environ):
        if key.startswith(prefix) :
            setattr(app, key[len(prefix):].lower(), os.environ[key])

    return app
