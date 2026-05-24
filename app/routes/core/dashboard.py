"""Vista del panel de usuario (dashboard).

Define la ruta `/dashboard` que muestra los documentos creados por el
usuario autenticado. Requiere que exista `usuario_id` en la sesión para
permitir el acceso; en caso contrario redirige al índice público.

Se consulta la colección `documentos_collection` para obtener los
documentos asociados al `usuario_id` presente en la sesión y se pasan
como contexto a la plantilla `dashboard.html`.
"""

from flask import render_template, session, redirect, url_for
from . import core_bp
from app.database import documentos_collection


@core_bp.route('/dashboard')
def dashboard():
    # Verificar que el usuario esté autenticado (tengamos su id en sesión).
    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    # Recuperar los documentos pertenecientes al usuario.
    mis_documentos = list(documentos_collection.find({
        "usuario_id": session['usuario_id']
    }))

    # Renderizar el dashboard con la lista de documentos.
    return render_template('dashboard.html', documentos=mis_documentos)