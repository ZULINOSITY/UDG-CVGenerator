# Como programar actualizaciones

Esta guia explica donde tocar el codigo cuando quieras agregar o cambiar funciones.

## Regla base

- Si cambia el comportamiento, revisa primero la ruta de Flask.
- Si cambia la interfaz, revisa templates, CSS y JS.
- Si cambia la informacion guardada, revisa el formulario, la ruta CRUD y la coleccion de MongoDB.

## Agregar un nuevo campo al CV

1. Agrega el campo en `app/templates/form.html`.
2. Lee el dato en `app/routes/crud/create.py` y `app/routes/crud/update.py`.
3. Si el dato debe mostrarse en la vista, actualiza las plantillas en `app/templates/plantillasCV/`.
4. Si el estilo cambia, ajusta `app/static/css/`.

## Agregar una nueva plantilla

1. Crea un archivo nuevo en `app/templates/plantillasCV/`.
2. Agrega una opcion en el selector de `app/templates/form.html`.
3. Verifica que `ver_cv` y `descargar_pdf` puedan resolver el nuevo nombre de plantilla.
4. Si hace falta, ajusta CSS especifico en `app/static/css/plantillas/`.

## Cambiar el flujo de guardado

- `nuevo_cv` crea documentos nuevos.
- `editar_cv` modifica documentos existentes.
- Si quieres cambiar la estructura de datos, haz el cambio en ambas rutas para que creen y actualicen el mismo esquema.

## Agregar una nueva ruta

1. Crea el archivo dentro del blueprint correcto.
2. Importalo desde el `__init__.py` del blueprint.
3. Registra el blueprint en `app/__init__.py` si es uno nuevo.
4. Agrega el enlace o boton en la plantilla correspondiente.

## Versiones y cambios

- Documenta cambios funcionales aqui antes de moverlos a produccion.
- Si una actualizacion toca datos existentes, prueba primero con un documento real y uno vacio.
