from flask import Flask

from looklike.blueprints.clothes_routes import clothes_bp


def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(clothes_bp)

    return app
