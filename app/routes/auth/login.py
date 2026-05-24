"""Rutas y lógica para el inicio de sesión de usuarios.

Este módulo define la ruta `/login` que muestra el formulario de inicio
de sesión (GET) y procesa las credenciales enviadas por el usuario (POST).

Flujo principal:
- GET: renderiza la plantilla `login.html` con el formulario.
- POST: obtiene `correo` y `password` del formulario, busca el usuario
  en la colección `usuarios_collection`, y verifica la contraseña usando
  `check_password_hash`.
- Si las credenciales son válidas, guarda información mínima en la
  `session` (`usuario_id`, `nombre`) y redirige al `core.dashboard`.
- Si fallan, muestra un mensaje (flash) y redirige nuevamente al login.

Dependencias:
- `usuarios_collection`: colección MongoDB definida en `app.database`.
- `auth_bp`: blueprint importado desde el paquete `auth`.
"""

from flask import request, redirect, url_for, session, flash, render_template
from werkzeug.security import check_password_hash
from . import auth_bp
from app.database import usuarios_collection


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Si es una petición GET, devolvemos el formulario de login.
    if request.method == 'GET':
        return render_template('login.html')

    # Si es POST, procesamos las credenciales del formulario.
    correo = request.form.get('correo')
    password = request.form.get('password')

    # Buscamos el usuario por correo en la base de datos.
    usuario = usuarios_collection.find_one({
        "correo": correo
    })

    # Verificamos que el usuario exista y que la contraseña coincida.
    if usuario and check_password_hash(
        usuario['password_hash'],
        password
    ):

        # Guardamos datos mínimos en la sesión para identificar al usuario.
        session['usuario_id'] = str(usuario['_id'])
        session['nombre'] = usuario['nombre']

        flash("Bienvenido")

        # Redirigimos al dashboard principal de la aplicación.
        return redirect(url_for('core.dashboard'))

    # Si no coincide, informamos y volvemos al formulario de login.
    flash("Credenciales incorrectas")

    return redirect(url_for('auth.login'))