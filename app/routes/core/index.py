from flask import render_template, session, redirect, url_for
from . import core_bp

@core_bp.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('core.dashboard'))
    return render_template('inicio.html')