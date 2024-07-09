document.addEventListener('DOMContentLoaded', function () {
    const toggleDetails = document.getElementById('toggle-details');
    const aboutDetails = document.getElementById('about-details');

    toggleDetails.addEventListener('click', function (event) {
        event.preventDefault();

        if (aboutDetails.style.display === 'block') {
            aboutDetails.style.display = 'none';
            toggleDetails.innerHTML = 'Ver detalles';
        } else {
            aboutDetails.style.display = 'block';
            toggleDetails.innerHTML = 'Ocultar detalles';
        }
    });
});
