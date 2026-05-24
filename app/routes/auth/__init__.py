from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

# Importamos los módulos para registrar las rutas
from . import login, register, logout