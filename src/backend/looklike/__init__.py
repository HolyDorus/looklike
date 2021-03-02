from flask import Flask, send_from_directory
from flask_cors import CORS

from looklike.blueprints.clothes_routes import clothes_bp
from looklike.blueprints.characters_routes import characters_bp


def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r'/*': {'origins': config_class.FRONTEND_URL}})

    app.register_blueprint(clothes_bp)
    app.register_blueprint(characters_bp)

    if app.config['DEBUG']:
        media_root = app.config['MEDIA_ROOT']
        media_url = app.config['MEDIA_URL']
        url = f'{media_url}<path:filename>'

        @app.route(url, methods=['GET'])
        def get_media(filename: str):
            return send_from_directory(media_root, filename)

    return app
