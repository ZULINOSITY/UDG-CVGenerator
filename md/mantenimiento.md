# Mantenimiento y despliegue

## Requisitos

- Python con Flask.
- MongoDB accesible desde `MONGO_URI`.
- Dependencias instaladas desde `modules.txt`.

## Variables de entorno

- `SECRET_KEY`
- `MONGO_URI`

## Arranque local

1. Instala dependencias.
2. Define las variables de entorno.
3. Ejecuta `run.py`.

## Puntos sensibles

- `app/database.py` depende de que MongoDB responda al iniciar.
- `descargar_pdf` depende de WeasyPrint y de que las plantillas HTML sean renderizables.
- El editor de `form.html` depende de `static/js/form.js` para sincronizar los campos ocultos.

## Buenas practicas

- Mantener nombres consistentes entre el formulario, la ruta y la plantilla.
- Probar login, alta, edicion, PDF y eliminacion despues de cada cambio grande.
- Si agregas campos nuevos, confirma que el dashboard y las plantillas no fallen con documentos antiguos.
