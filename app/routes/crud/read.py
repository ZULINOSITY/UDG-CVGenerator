"""Vistas para visualizar y descargar CVs del usuario.

Contiene dos rutas principales:
- `ver_cv`: renderiza el CV en HTML usando la plantilla seleccionada.
- `descargar_pdf`: renderiza la misma plantilla y la convierte a PDF
  usando WeasyPrint, devolviéndola como respuesta HTTP.

Ambas rutas comprueban que el `usuario_id` esté en la sesión y que el
documento consultado pertenezca al usuario autenticado. Si no se cumple,
se redirige al dashboard o índice según corresponda.
"""

from flask import render_template, session, redirect, url_for, request, make_response, flash
from bson.objectid import ObjectId
from weasyprint import HTML
from . import cv_bp
from app.database import documentos_collection


@cv_bp.route('/ver_cv/<id_doc>')
def ver_cv(id_doc):

    # Requerir que el usuario esté autenticado.
    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    # Buscar el documento por _id y usuario_id para asegurar propiedad.
    documento = documentos_collection.find_one({
        "_id": ObjectId(id_doc),
        "usuario_id": session['usuario_id']
    })

    # Si no existe o no pertenece al usuario, informar y volver al dashboard.
    if not documento:
        flash("Documento no encontrado")
        return redirect(url_for('core.dashboard'))

    # Seleccionar la plantilla indicada en el documento (valor por defecto).
    nombre_plantilla = documento.get('plantilla', 'convencional')

    # Renderizar la plantilla correspondiente dentro de `plantillasCV/`.
    return render_template(
        f'plantillasCV/{nombre_plantilla}.html',
        doc=documento
    )


@cv_bp.route('/descargar_pdf/<id_doc>')
def descargar_pdf(id_doc):

    # Requerir que el usuario esté autenticado.
    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    # Recuperar el documento asegurando que pertenece al usuario.
    documento = documentos_collection.find_one({
        "_id": ObjectId(id_doc),
        "usuario_id": session['usuario_id']
    })

    if not documento:
        return redirect(url_for('core.dashboard'))

    # Plantilla por defecto usada para generar el PDF.
    plantilla = documento.get('plantilla', 'estetico')

    # Renderizar HTML de la plantilla con el contexto del documento.
    html = render_template(
        f'plantillasCV/{plantilla}.html',
        doc=documento
    )

    # Convertir el HTML a PDF con WeasyPrint, resolviendo recursos relativos
    # usando `request.host_url` como base.
    pdf = HTML(
        string=html,
        base_url=request.host_url
    ).write_pdf()

    # Construir un nombre de archivo seguro a partir de `nombre_completo`.
    nombre_archivo = documento.get("nombre_completo", "CV")
    nombre_archivo = (
        nombre_archivo
        .replace('\n', '')
        .replace('\r', '')
        .replace('<br>', ' ')
        .strip()
    )

    safe_name = "".join(
        c for c in nombre_archivo
        if c.isalnum() or c in (' ', '-', '_')
    ).strip()

    # Preparar la respuesta HTTP con el PDF y cabeceras apropiadas.
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = (
        f'inline; filename="{safe_name}.pdf"'
    )

    return response