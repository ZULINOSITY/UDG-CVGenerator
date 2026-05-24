from flask import render_template, session, redirect, url_for, request, make_response, flash
from bson.objectid import ObjectId
from weasyprint import HTML
from . import cv_bp
from app.database import documentos_collection


@cv_bp.route('/ver_cv/<id_doc>')
def ver_cv(id_doc):

    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    documento = documentos_collection.find_one({
        "_id": ObjectId(id_doc),
        "usuario_id": session['usuario_id']
    })

    if not documento:
        flash("Documento no encontrado")
        return redirect(url_for('core.dashboard'))

    nombre_plantilla = documento.get('plantilla', 'convencional')

    return render_template(
        f'plantillasCV/{nombre_plantilla}.html',
        doc=documento
    )


@cv_bp.route('/descargar_pdf/<id_doc>')
def descargar_pdf(id_doc):

    if 'usuario_id' not in session:
        return redirect(url_for('core.index'))

    documento = documentos_collection.find_one({
        "_id": ObjectId(id_doc),
        "usuario_id": session['usuario_id']
    })

    if not documento:
        return redirect(url_for('core.dashboard'))

    plantilla = documento.get('plantilla', 'estetico')

    html = render_template(
        f'plantillasCV/{plantilla}.html',
        doc=documento
    )

    pdf = HTML(
        string=html,
        base_url=request.host_url
    ).write_pdf()

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

    response = make_response(pdf)

    response.headers['Content-Type'] = 'application/pdf'

    response.headers['Content-Disposition'] = (
        f'inline; filename="{safe_name}.pdf"'
    )

    return response