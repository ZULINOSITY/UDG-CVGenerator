from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Importación ajustada a la nueva estructura de carpetas
    from app.routes.auth import auth_bp
    from app.routes.core import core_bp
    from app.routes.crud import cv_bp


    app.register_blueprint(auth_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(cv_bp)

    return app