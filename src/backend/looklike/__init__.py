from flask import Flask

from looklike.configs import config
from looklike.blueprints.clothes_routes import clothes_bp
from looklike.blueprints.characters_routes import characters_bp
from looklike.blueprints.users_routes import users_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(clothes_bp)
    app.register_blueprint(characters_bp)
    app.register_blueprint(users_bp)

    return app
