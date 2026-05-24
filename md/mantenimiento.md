# Mantenimiento y despliegue

## Requisitos

- Python con Flask.
- MongoDB accesible desde `MONGO_URI`.
- Dependencias instaladas desde `modules.txt`.
- Compilador GTK3 para Windows
- Inicializar .env

## Variables de entorno

- `SECRET_KEY`
- `MONGO_URI`

### Instalación de compilador en el equipo.
1. Descargar instalador de compilador de GTK3.
2. https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases/download/2022-01-04/gtk3-runtime-3.24.31-2022-01-04-ts-win64.exe
3. Ejecutar y spamear Next.

### Instalación de modulos para python.
1. Ejecutar pip con el siguiente comando en la terminal del proyecto.
2. `pip install -r modules.txt`

## Arranque local

Ejecuta `run.py`


## Puntos sensibles

- `app/database.py` depende de que MongoDB responda al iniciar.
- `descargar_pdf` depende de WeasyPrint y de que las plantillas HTML sean renderizables.
- El editor de `form.html` depende de `static/js/form.js` para sincronizar los campos ocultos.

## Buenas practicas

- Mantener nombres consistentes entre el formulario, la ruta y la plantilla.
- Probar login, alta, edicion, PDF y eliminacion despues de cada cambio grande.
- Si agregas campos nuevos, confirma que el dashboard y las plantillas no fallen con documentos antiguos.
