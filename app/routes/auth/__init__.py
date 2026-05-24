"""Módulo de inicialización del blueprint de autenticación.

Este archivo crea y configura el blueprint `auth_bp` usado para agrupar
todas las rutas relacionadas con autenticación (login, registro, logout).
Al importarse, también registra los submódulos `login`, `register` y `logout`
para que Flask descubra las rutas definidas en ellos.

Uso:
- `auth_bp` se monta en la aplicación principal desde `app/__init__.py` o
	desde el punto donde se registre el blueprint.
"""

from flask import Blueprint

# Creamos el blueprint para las rutas de autenticación.
# Nombre: 'auth' (usado en `url_for('auth.<endpoint>')`)
# `__name__` permite a Flask localizar recursos estáticos y templates relativos.
auth_bp = Blueprint('auth', __name__)

# Importamos los módulos que definen las rutas concretas de autenticación.
# Estos imports deben ir después de crear `auth_bp` para que las rutas se
# registren correctamente cuando se importe este paquete.
from . import login, register, logout