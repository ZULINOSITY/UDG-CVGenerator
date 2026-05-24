"""Módulo de inicialización del blueprint `core`.

Este archivo crea el blueprint `core_bp` que agrupa las rutas principales
de la aplicación (página de inicio, dashboard, etc.). Al importarlo se
registran los submódulos `index` y `dashboard` que definen las rutas
concretas.

`core_bp` suele montarse en la aplicación principal para exponer
las vistas públicas y las vistas protegidas por sesión.
"""

from flask import Blueprint

# Blueprint para las rutas principales (core) de la aplicación.
core_bp = Blueprint('core', __name__)

# Importar los módulos que contienen las rutas específicas.
from . import index, dashboard