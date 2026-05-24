/*
  Script de interacción para el formulario de edición/creación de CV.

  Funcionalidades principales:
  - Cambio dinámico de plantilla para la vista previa del CV.
  - Campos editables sincronizados entre la vista previa y campos ocultos
    del formulario (`hidden_*`) para que se envíen al servidor.
  - Guardado del documento mediante `guardarDocumento()` que sincroniza
    la plantilla seleccionada con un campo oculto y envía el formulario.
  - Previsualización y compresión de la foto antes de incrustarla en el
    formulario (se guarda como Base64 JPEG comprimido en `hidden_foto`).
*/

document.addEventListener('DOMContentLoaded', () => {

    /* ========================================= */
    /* CAMBIO DE PLANTILLA DINÁMICO */
    /* ========================================= */

    const selector = document.getElementById('select_plantilla');
    const plantillas = document.querySelectorAll('.cv-preview-wrapper');

    function actualizarVistaPlantilla() {
        if (!selector) return;
        const idSeleccionado = 'tpl_' + selector.value;

        plantillas.forEach(wrapper => {
            wrapper.style.display = (wrapper.id === idSeleccionado) ? 'block' : 'none';
        });
    }

    // Carga inicial basada en la plantilla guardada en la base de datos
    actualizarVistaPlantilla();

    // Actualización cuando el usuario cambia el selector
    if (selector) {
        selector.addEventListener('change', actualizarVistaPlantilla);
    }

    /* ========================================= */
    /* CAMPOS EDITABLES */
    /* ========================================= */

    // Selecciona todos los elementos que representan campos editables
    const campos = document.querySelectorAll('[data-field]');

    campos.forEach(campo => {

        const tipoCampo = campo.getAttribute('data-field');
        const hiddenInput = document.getElementById('hidden_' + tipoCampo);

        /* INICIALIZAR: si el input oculto está vacío, poblarlo con el contenido */
        if (hiddenInput && !hiddenInput.value) {
            hiddenInput.value = campo.innerHTML.trim();
        }

        /* ACTIVAR EDICION IN-SITU */
        campo.setAttribute('contenteditable', 'true');

        /* ESCUCHAR CAMBIOS Y SINCRONIZAR */
        campo.addEventListener('input', function () {

            const valorActual = this.innerHTML;

            /* SINCRONIZAR ELEMENTOS GEMELOS que compartan el mismo data-field */
            document.querySelectorAll(`[data-field="${tipoCampo}"]`).forEach(gemelo => {
                if (gemelo !== this) {
                    gemelo.innerHTML = valorActual;
                }
            });

            /* ACTUALIZAR INPUT OCULTO para que el servidor reciba el valor */
            if (hiddenInput) {
                hiddenInput.value = valorActual;
            }

        });

    });    

    // Inicializar hidden_foto desde la imagen ya renderizada en la vista previa
    (function inicializarHiddenFoto() {
        const hiddenFoto = document.getElementById('hidden_foto');
        if (!hiddenFoto || hiddenFoto.value) return;
    
        // Buscar la primera imagen de la vista previa (cubre distintas plantillas)
        const previewImg = document.querySelector('.cv-preview-wrapper img')
                         || document.querySelector('.photo img')
                         || document.querySelector('.photo-preview');
    
        if (previewImg && previewImg.src) {
            hiddenFoto.value = previewImg.src;
        }
    })();

});

/* ========================================= */
/* GUARDAR DOCUMENTO */
/* ========================================= */

function guardarDocumento() {
    const selector = document.getElementById('select_plantilla');
    const form = document.getElementById('formGuardar');
    const hiddenPlantilla = document.getElementById('hidden_plantilla');

    if (selector && form && hiddenPlantilla) {
        // Sincronizar la plantilla seleccionada en el campo oculto y enviar
        hiddenPlantilla.value = selector.value;
        form.submit();
    }
}

/* ========================================= */
/* PREVISUALIZAR Y GUARDAR FOTO */
/* ========================================= */

function previsualizarFoto(event) {
    const file = event.target.files && event.target.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            // 1. Crear una imagen en memoria para obtener sus dimensiones
            const img = new Image();

            img.onload = function () {
                // 2. Crear un canvas para redimensionar la imagen manteniendo proporciones
                const canvas = document.createElement('canvas');
                const MAX_WIDTH = 400; // Tamaño máximo recomendado para el CV
                const MAX_HEIGHT = 400;
                let width = img.width;
                let height = img.height;

                // 3. Ajustar dimensiones preservando la relación de aspecto
                if (width > height) {
                    if (width > MAX_WIDTH) {
                        height *= MAX_WIDTH / width;
                        width = MAX_WIDTH;
                    }
                } else {
                    if (height > MAX_HEIGHT) {
                        width *= MAX_HEIGHT / height;
                        height = MAX_HEIGHT;
                    }
                }

                // 4. Dibujar la imagen redimensionada en el canvas
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                // 5. Comprimir a JPEG con calidad 0.7 para reducir tamaño
                const dataUrlComprimida = canvas.toDataURL('image/jpeg', 0.7);

                /* ACTUALIZAR TODAS LAS FOTOS EN LA VISTA PREVIA */
                document.querySelectorAll('.photo').forEach(el => {
                    el.innerHTML = `<img src="${dataUrlComprimida}" class="photo-preview">`;
                });

                /* GUARDAR BASE64 COMPRIMIDO EN EL INPUT OCULTO */
                const hiddenFoto = document.getElementById('hidden_foto');
                if (hiddenFoto) {
                    hiddenFoto.value = dataUrlComprimida;
                }
            };

            // Iniciar la carga de la imagen desde el FileReader
            img.src = e.target.result;
        }

        reader.readAsDataURL(file);
    }
}