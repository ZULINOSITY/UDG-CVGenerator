"""Vistas públicas de la aplicación: página de inicio.

Define la ruta raíz `/` que actúa como página de inicio. Si el usuario ya
está autenticado (tiene `usuario_id` en la sesión), se le redirige al
`dashboard`. En caso contrario, se renderiza la plantilla pública
`inicio.html`.
"""

from flask import render_template, session, redirect, url_for
from . import core_bp


@core_bp.route('/')
def index():
    # Si hay un usuario en sesión, ir al dashboard en vez de la página pública.
    if 'usuario_id' in session:
        return redirect(url_for('core.dashboard'))

    # Mostrar la página de inicio para usuarios no autenticados.
    return render_template('inicio.html')