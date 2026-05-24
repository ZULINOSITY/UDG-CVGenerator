"""Inicialización del blueprint para operaciones CRUD sobre CVs.

Este paquete agrupa las rutas para crear, leer, actualizar y eliminar
documentos (CVs). Se expone el blueprint `cv_bp` que se registra en la
aplicación principal para organizar las rutas relacionadas con los CVs.
"""

from flask import Blueprint

# Blueprint llamado 'cv' para las operaciones CRUD de los CVs.
cv_bp = Blueprint('cv', __name__)

# Importar los módulos que implementan las operaciones CRUD.
from . import create, read, update, delete