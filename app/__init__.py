"""Inicialización de la aplicación Flask.

Este módulo define la fábrica `create_app()` que construye y configura
la aplicación Flask, carga la configuración desde `Config` y registra
los blueprints que contienen las rutas de la aplicación (`auth`,
`core`, `cv`). Usar una fábrica facilita la configuración en pruebas y
despliegue.
"""

from flask import Flask
from config import Config


def create_app():
    """Crear y configurar la aplicación Flask.

    - Crea la instancia `Flask`.
    - Carga la configuración desde la clase `Config` (archivo `config.py`).
    - Importa y registra los blueprints: `auth_bp`, `core_bp`, `cv_bp`.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Importar blueprints desde los paquetes de rutas. Hacemos los
    # imports aquí (dentro de la fábrica) para evitar dependencias cíclicas
    # durante la inicialización del paquete.
    from app.routes.auth import auth_bp
    from app.routes.core import core_bp
    from app.routes.crud import cv_bp

    # Registrar blueprints en la aplicación
    app.register_blueprint(auth_bp)
    app.register_blueprint(core_bp)
    app.register_blueprint(cv_bp)

    return app