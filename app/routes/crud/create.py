from flask import request, redirect, url_for, session, flash, render_template
from . import cv_bp
from app.database import documentos_collection

@cv_bp.route('/nuevo_cv', methods=['GET', 'POST'])
def nuevo_cv():
    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    if request.method == 'POST':
        nuevo_documento = {
            "tipo_documento": "cv",
            "usuario_id": session['usuario_id'],
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
        documentos_collection.insert_one(nuevo_documento)
        flash("CV guardado correctamente")
        return redirect(url_for('core.dashboard'))

    doc_vacio = {k: "" for k in ["nombre_completo", "profesion", "telefono", "email", "perfil", "experiencia", "educacion", "habilidades", "idiomas", "referencias", "foto"]}
    doc_vacio["plantilla"] = "convencional"
    return render_template('form.html', doc=doc_vacio)