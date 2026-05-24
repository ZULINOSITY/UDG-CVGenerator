"""Ruta para cerrar la sesión del usuario.

Aquí se define la ruta `/logout` que limpia la sesión del usuario y lo
redirige a la página principal de la aplicación (`core.index`). Se usa
`session.clear()` para eliminar todos los datos almacenados en la sesión.
"""

from flask import redirect, url_for, session
from . import auth_bp


@auth_bp.route('/logout')
def logout():
    # Eliminamos toda la información de la sesión del usuario.
    session.clear()

    # Redirigimos a la página de inicio (o índice) del módulo `core`.
    return redirect(url_for('core.index'))