document.addEventListener('DOMContentLoaded', () => {
    const toasts = document.querySelectorAll('.toast');

    toasts.forEach((toast, index) => {
        const delay = 3200 + (index * 250);

        window.setTimeout(() => {
            toast.style.transition = 'opacity 220ms ease, transform 220ms ease, max-height 220ms ease, margin 220ms ease, padding 220ms ease';
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(-.35rem)';
            toast.style.maxHeight = '0';
            toast.style.margin = '0';
            toast.style.paddingTop = '0';
            toast.style.paddingBottom = '0';
            toast.style.borderWidth = '0';

            window.setTimeout(() => {
                toast.remove();

                const container = document.querySelector('.toast-container');
                if (container && container.children.length === 0) {
                    container.remove();
                }
            }, 240);
        }, delay);
    });
});