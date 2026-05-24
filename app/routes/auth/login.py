from flask import request, redirect, url_for, session, flash, render_template
from werkzeug.security import check_password_hash
from . import auth_bp
from app.database import usuarios_collection

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # MOSTRAR FORMULARIO
    if request.method == 'GET':
        return render_template('login.html')

    # PROCESAR LOGIN
    correo = request.form.get('correo')
    password = request.form.get('password')

    usuario = usuarios_collection.find_one({
        "correo": correo
    })

    if usuario and check_password_hash(
        usuario['password_hash'],
        password
    ):

        session['usuario_id'] = str(usuario['_id'])
        session['nombre'] = usuario['nombre']

        flash("Bienvenido")

        return redirect(url_for('core.dashboard'))

    flash("Credenciales incorrectas")

    return redirect(url_for('auth.login'))