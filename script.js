// JavaScript para mostrar/ocultar los detalles adicionales al hacer clic en "Ver detalles"
        const toggleDetails = document.getElementById('toggle-details');
        const aboutDetails = document.getElementById('about-details');

        toggleDetails.addEventListener('click', function(event) {
            event.preventDefault(); // Evita que el enlace navegue

            // Alternar la visibilidad de los detalles adicionales
            aboutDetails.classList.toggle('collapsed');

            // Cambiar el texto del enlace y girar el ícono según el estado de visualización
            if (aboutDetails.classList.contains('collapsed')) {
                toggleDetails.innerHTML = 'Ver detalles <i class="fas fa-chevron-down"></i>';
            } else {
                toggleDetails.innerHTML = 'Ocultar detalles <i class="fas fa-chevron-up"></i>';
            }
