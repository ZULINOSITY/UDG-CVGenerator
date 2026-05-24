"""Eliminar un CV del usuario autenticado.

Define la ruta `/eliminar/<id_doc>` que acepta sólo `POST`. Verifica que
el usuario esté autenticado (tenga `usuario_id` en la sesión) y elimina
el documento cuya `_id` coincide con `id_doc` y que pertenezca al
usuario actual. Usar la condición `usuario_id` en la consulta evita que
un usuario elimine documentos de otro.
"""

from flask import redirect, url_for, session, flash
from bson.objectid import ObjectId
from . import cv_bp
from app.database import documentos_collection


@cv_bp.route('/eliminar/<id_doc>', methods=['POST'])
def eliminar_cv(id_doc):
    # Solo permitir la eliminación si hay un usuario autenticado.
    if 'usuario_id' in session:
        # Convertir el id a ObjectId y eliminar solo si pertenece al usuario.
        documentos_collection.delete_one({"_id": ObjectId(id_doc), "usuario_id": session['usuario_id']})
        flash("Documento eliminado")

    # Redirigir al dashboard en todos los casos.
    return redirect(url_for('core.dashboard'))