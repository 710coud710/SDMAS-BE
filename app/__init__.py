from flask import Flask
from .config import Config
from .routes.auth import auth_bp
from .routes.members import members_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(members_bp, url_prefix='/api')

    return app
