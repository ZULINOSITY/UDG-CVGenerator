from flask import render_template, session, redirect, url_for
from . import core_bp
from app.database import documentos_collection

@core_bp.route('/dashboard')
def dashboard():
    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    mis_documentos = list(documentos_collection.find({
        "usuario_id": session['usuario_id']
    }))

    return render_template('dashboard.html', documentos=mis_documentos)