/* =========================================
   CARGA INICIAL Y SINCRONIZACIÓN
========================================= */

document.addEventListener('DOMContentLoaded', () => {

    /* ========================================= */
    /* CAMBIO DE PLANTILLA DINÁMICO */
    /* ========================================= */

    const selector = document.getElementById('select_plantilla');
    const plantillas = document.querySelectorAll('.cv-preview-wrapper');

    function actualizarVistaPlantilla() {
        const idSeleccionado = 'tpl_' + selector.value;

        plantillas.forEach(wrapper => {
            wrapper.style.display = (wrapper.id === idSeleccionado) ? 'block' : 'none';
        });
    }

    // Carga inicial basada en la base de datos
    actualizarVistaPlantilla();

    // Actualización al cambiar el selector
    if (selector) {
        selector.addEventListener('change', actualizarVistaPlantilla);
    }

    /* ========================================= */
    /* CAMPOS EDITABLES */
    /* ========================================= */

    const campos = document.querySelectorAll('[data-field]');

    campos.forEach(campo => {

        const tipoCampo = campo.getAttribute('data-field');
        const hiddenInput = document.getElementById('hidden_' + tipoCampo);

        /* INICIALIZAR */
        if(hiddenInput && !hiddenInput.value){
            hiddenInput.value = campo.innerHTML.trim();
        }

        /* ACTIVAR EDICION */
        campo.setAttribute('contenteditable', 'true');

        /* ESCUCHAR CAMBIOS */
        campo.addEventListener('input', function(){

            const valorActual = this.innerHTML;

            /* SINCRONIZAR GEMELOS */
            document.querySelectorAll(`[data-field="${tipoCampo}"]`).forEach(gemelo => {
                if(gemelo !== this){
                    gemelo.innerHTML = valorActual;
                }
            });

            /* ACTUALIZAR INPUT */
            if(hiddenInput){
                hiddenInput.value = valorActual;
            }

        });

    });

});

/* ========================================= */
/* GUARDAR DOCUMENTO */
/* ========================================= */

function guardarDocumento(){
    const selector = document.getElementById('select_plantilla');
    const form = document.getElementById('formGuardar');
    const hiddenPlantilla = document.getElementById('hidden_plantilla');
    
    if (selector && form && hiddenPlantilla) {
        hiddenPlantilla.value = selector.value;
        form.submit();
    }
}

/* ========================================= */
/* PREVISUALIZAR Y GUARDAR FOTO */
/* ========================================= */

function previsualizarFoto(event){
    const file = event.target.files[0];

    if(file){
        const reader = new FileReader();

        reader.onload = function(e){
            // 1. Creamos una imagen virtual en memoria
            const img = new Image();
            
            img.onload = function() {
                // 2. Creamos un "lienzo" (canvas) para redibujar la foto más pequeña
                const canvas = document.createElement('canvas');
                const MAX_WIDTH = 400; // Tamaño máximo ideal para un CV
                const MAX_HEIGHT = 400;
                let width = img.width;
                let height = img.height;

                // 3. Calculamos las nuevas proporciones
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

                // 4. Ajustamos el lienzo e incrustamos la imagen
                canvas.width = width;
                canvas.height = height;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, width, height);

                // 5. COMPRESIÓN MÁGICA: Convertimos a formato JPEG con 70% de calidad
                const dataUrlComprimida = canvas.toDataURL('image/jpeg', 0.7);

                /* ACTUALIZAR TODAS LAS FOTOS EN PANTALLA */
                document.querySelectorAll('.photo').forEach(el => {
                    el.innerHTML = `<img src="${dataUrlComprimida}" class="photo-preview">`;
                });

                /* GUARDAR BASE64 YA COMPRIMIDO EN EL FORMULARIO */
                const hiddenFoto = document.getElementById('hidden_foto');
                if(hiddenFoto){
                    hiddenFoto.value = dataUrlComprimida;
                }
            };

            // Disparamos la carga de la imagen
            img.src = e.target.result;
        }

        reader.readAsDataURL(file);
    }
}