"""Editar un CV existente del usuario autenticado.

Ruta: `/editar_cv/<id_doc>` — permite a un usuario ver el formulario
con los datos actuales de un CV (GET) y guardar cambios (POST).

Comportamiento:
- Verifica que haya `usuario_id` en la sesión y que el documento
  exista y pertenezca al usuario.
- En POST recoge los campos del formulario, construye un diccionario
  `datos_actualizados` y aplica un `update_one` con `$set` sobre el
  documento identificado por `_id`.
- Después de actualizar redirige al `core.dashboard` mostrando un
  `flash` de confirmación.
"""

from flask import request, redirect, url_for, session, flash, render_template
from bson.objectid import ObjectId
from . import cv_bp
from app.database import documentos_collection


@cv_bp.route('/editar_cv/<id_doc>', methods=['GET', 'POST'])
def editar_cv(id_doc):
    # Requerir autenticación
    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    # Obtener el documento y verificar la propiedad (usuario_id)
    documento = documentos_collection.find_one({"_id": ObjectId(id_doc), "usuario_id": session['usuario_id']})

    if not documento:
        flash("Documento no encontrado")
        return redirect(url_for('core.dashboard'))

    # Procesar actualización enviada por POST
    if request.method == 'POST':
        datos_actualizados = {
            "nombre_completo": request.form.get('nombreCompleto'),
            "profesion": request.form.get('profesion'),
            "telefono": request.form.get('telefono'),
            "email": request.form.get('email'),
            "perfil": request.form.get('perfil'),
            "experiencia": request.form.get('experiencia'),
            "educacion": request.form.get('educacion'),
            "habilidades": request.form.get('habilidades'),
            "idiomas": request.form.get('idiomas'),
            "referencias": request.form.get('referencias'),
            "foto": request.form.get('foto'),
            "plantilla": request.form.get('plantilla', 'convencional')
        }
        documentos_collection.update_one({"_id": ObjectId(id_doc)}, {"$set": datos_actualizados})
        flash("Documento actualizado")
        return redirect(url_for('core.dashboard'))

    # GET: renderizar formulario con los datos actuales del documento
    return render_template('form.html', doc=documento)