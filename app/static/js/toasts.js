/*
  Módulo de toasts (notificaciones temporales).

  Comportamiento:
  - Cuando el DOM está listo, busca todos los elementos con clase
    `.toast` y configura un temporizador para cada uno.
  - Cada toast se oculta con una transición CSS (opacidad, transformación,
    altura máxima, márgenes y padding) después de un `delay` calculado.
  - Tras completar la transición se elimina el elemento del DOM. Si el
    contenedor de toasts queda vacío, también se elimina.

  Notas de implementación:
  - `delay` = 3200ms + 250ms * índice, de modo que los toasts aparecen
    y desaparecen escalonados si hay varios.
  - La segunda llamada a `setTimeout` (240ms) espera a que termine la
    transición antes de eliminar el elemento.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Seleccionar todos los toasts visibles en la página
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach((toast, index) => {
        // Calcular un retraso escalonado para cada toast
        const delay = 3200 + (index * 250);

        window.setTimeout(() => {
            // Aplicar la transición CSS para ocultar suavemente el toast
            toast.style.transition = 'opacity 220ms ease, transform 220ms ease, max-height 220ms ease, margin 220ms ease, padding 220ms ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-.35rem)';
            toast.style.maxHeight = '0';
            toast.style.margin = '0';
            toast.style.paddingTop = '0';
            toast.style.paddingBottom = '0';
            toast.style.borderWidth = '0';

            // Tras la duración de la transición, eliminar el elemento del DOM
            window.setTimeout(() => {
                toast.remove();

                // Si el contenedor queda vacío, eliminar también el contenedor
                const container = document.querySelector('.toast-container');
                if (container && container.children.length === 0) {
                    container.remove();
                }
            }, 240);
        }, delay);
    });
});