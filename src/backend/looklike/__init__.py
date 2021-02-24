from flask import Flask

from .blueprints.test_routes import test_bp


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(test_bp)

    return app
