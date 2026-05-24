"""Punto de entrada para ejecutar la aplicación localmente.

Este archivo prepara ligeras dependencias de plataforma (como directorios
con DLLs en Windows), crea la aplicación mediante la fábrica
`create_app()` y la ejecuta en modo de depuración cuando se ejecuta
directamente (`python run.py`).

No contiene lógica de negocio; su responsabilidad es inicializar y
arrancar la aplicación en entornos de desarrollo.
"""

import os
import sys

# Ruta base del proyecto (carpeta que contiene este archivo)
base_dir = os.path.dirname(os.path.abspath(__file__))
# Ruta opcional donde se pueden colocar DLLs necesarias en Windows
dlls_path = os.path.join(base_dir, "dlls")

# En Windows, si existe la carpeta `dlls`, añadirla al search path de DLLs
# para que dependencias nativas sean encontradas por el intérprete.
if sys.platform == 'win32' and os.path.exists(dlls_path):
    os.add_dll_directory(dlls_path)


from app import create_app

# Crear la aplicación mediante la fábrica definida en `app/__init__.py`
app = create_app()


if __name__ == '__main__':
    # Ejecutar la app en modo desarrollo (debug=True). En producción se
    # debe usar un servidor WSGI (gunicorn, waitress, etc.) y desactivar
    # el modo debug.
    app.run(debug=True)