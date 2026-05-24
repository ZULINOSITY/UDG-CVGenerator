from flask import request, redirect, url_for, session, flash, render_template
from bson.objectid import ObjectId
from . import cv_bp
from app.database import documentos_collection

@cv_bp.route('/editar_cv/<id_doc>', methods=['GET', 'POST'])
def editar_cv(id_doc):
    if 'usuario_id' not in session: return redirect(url_for('core.index'))
    documento = documentos_collection.find_one({"_id": ObjectId(id_doc), "usuario_id": session['usuario_id']})
    
    if not documento:
        flash("Documento no encontrado"); return redirect(url_for('core.dashboard'))

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

    return render_template('form.html', doc=documento)