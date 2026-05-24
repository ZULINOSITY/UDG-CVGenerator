# Arquitectura general

UDG CVGenerator es una aplicacion Flask conectada a MongoDB. La logica principal se divide en tres capas:

## 1. Arranque de la aplicacion

- `run.py` crea la app llamando a `create_app()`.
- `app/__init__.py` configura Flask y registra los blueprints.
- La app arranca en modo debug cuando se ejecuta el archivo principal.

## 2. Datos

- `app/database.py` abre la conexion a MongoDB con `MONGO_URI`.
- La base usada es `proyecto_cv`.
- Las colecciones principales son `usuarios` y `documentos`.

## 3. Rutas

- `app/routes/auth/` maneja login, registro y logout.
- `app/routes/core/` maneja la pagina inicial y el dashboard.
- `app/routes/crud/` maneja crear, leer, actualizar, eliminar, ver PDF y renderizar CV.

## 4. Presentacion

- `app/templates/` contiene las vistas HTML.
- `app/static/css/` y `app/static/js/` contienen estilos y comportamiento del editor.
- Las plantillas de CV viven en `app/templates/plantillasCV/`.
