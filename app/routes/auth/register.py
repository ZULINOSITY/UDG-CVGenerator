from flask import request, redirect, url_for, flash, render_template
from werkzeug.security import generate_password_hash
from . import auth_bp
from app.database import usuarios_collection

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    password = request.form.get('password')

    if usuarios_collection.find_one({"correo": correo}):
        flash("Ese correo ya existe")
        return redirect(url_for('auth.register'))

    usuarios_collection.insert_one({
        "nombre": nombre,
        "correo": correo,
        "password_hash": generate_password_hash(password)
    })
    flash("Cuenta creada correctamente")
    return redirect(url_for('core.index'))