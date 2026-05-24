    /*
      Script para la navegación en la página de inicio.

      Funcionalidades:
      - Alternar el menú de navegación (`navMenu`) al pulsar el botón
        `menuToggle`.
      - Cerrar el menú al hacer clic fuera de él.
      - Cerrar el menú con la tecla Escape.

      El código asume que existen los elementos con ids `navMenu` y
      `menuToggle`; si no existen el script no fallará porque se comprueba
      su presencia antes de añadir listeners.
    */

    const navMenu = document.getElementById('navMenu');
    const menuToggle = document.getElementById('menuToggle');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            const isOpen = navMenu.classList.toggle('open');
            // `aria-expanded` espera 'true'/'false' como string
            menuToggle.setAttribute('aria-expanded', String(isOpen));
        });

        // Cerrar al hacer clic fuera del menú
        document.addEventListener('click', (e) => {
            if (!navMenu.contains(e.target)) {
                navMenu.classList.remove('open');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });

        // Cerrar con la tecla Escape
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                navMenu.classList.remove('open');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    }