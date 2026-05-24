from flask import Blueprint

cv_bp = Blueprint('cv', __name__)

from . import create, read, update, delete