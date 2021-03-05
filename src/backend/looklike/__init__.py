from flask import Flask, send_from_directory

from looklike.blueprints.clothes_routes import clothes_bp
from looklike.blueprints.characters_routes import characters_bp
from looklike.extensions import cors


def create_app(config_class) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    cors.init_app(app)

    app.register_blueprint(clothes_bp)
    app.register_blueprint(characters_bp)

    if app.config['ENABLE_MEDIA_FILES']:
        connect_media_folder(app)

    return app


def connect_media_folder(app):
    media_root = app.config['MEDIA_ROOT']
    media_url = app.config['MEDIA_URL']
    
    if media_root and media_url:
        url = f'{media_url}<path:filename>'

        @app.route(url, methods=['GET'])
        def get_media(filename: str):
            return send_from_directory(media_root, filename)
