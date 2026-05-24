from flask import redirect, url_for, session, flash
from bson.objectid import ObjectId
from . import cv_bp
from app.database import documentos_collection

@cv_bp.route('/eliminar/<id_doc>', methods=['POST'])
def eliminar_cv(id_doc):
    if 'usuario_id' in session:
        documentos_collection.delete_one({"_id": ObjectId(id_doc), "usuario_id": session['usuario_id']})
        flash("Documento eliminado")
    return redirect(url_for('core.dashboard'))