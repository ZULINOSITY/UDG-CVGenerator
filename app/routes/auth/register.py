"""Rutas y lógica para registrar nuevos usuarios.

Este módulo define la ruta `/register` que muestra el formulario de
registro (GET) y procesa la creación de una nueva cuenta (POST).

Flujo principal:
- GET: renderiza la plantilla `register.html` con el formulario.
- POST: recoge `nombre`, `correo` y `password` del formulario.
  - Comprueba si ya existe un usuario con el mismo correo.
  - Si no existe, crea un documento en `usuarios_collection` con el
    `nombre`, `correo` y un `password_hash` generado mediante
    `generate_password_hash`.
  - Muestra mensajes informativos con `flash` y redirige según el caso.

Notas de seguridad:
- Se almacena únicamente el hash de la contraseña (`password_hash`),
  nunca la contraseña en texto claro.
"""

from flask import request, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash
from . import auth_bp
from app.database import usuarios_collection


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Mostrar formulario de registro
    if request.method == 'GET':
        return render_template('register.html')

    # Procesar datos enviados por POST desde el formulario
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    password = request.form.get('password')

    # Comprobar si ya existe un usuario con el correo proporcionado
    if usuarios_collection.find_one({"correo": correo}):
        flash("Ese correo ya existe")
        return redirect(url_for('auth.register'))

    # Insertar nuevo usuario con la contraseña hasheada
    usuarios_collection.insert_one({
        "nombre": nombre,
        "correo": correo,
        "password_hash": generate_password_hash(password)
    })

    flash("Cuenta creada correctamente")
    return redirect(url_for('core.index'))