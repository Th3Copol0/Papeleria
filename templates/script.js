
// Función para mostrar la notificación
function showNotification(message) {
    var notification = document.createElement('div');
    notification.classList.add('notification');
    notification.textContent = message;
    document.body.appendChild(notification);

    // Temporizador para ocultar la notificación después de 5 segundos
    setTimeout(function() {
        notification.classList.add('slideOutRight');
        setTimeout(function() {
            notification.remove();
        }, 500); // Espera 0.5 segundos para remover la notificación
    }, 5000); // Espera 5 segundos antes de iniciar la animación de salida
}

// Mostrar una notificación de prueba al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    showNotification('¡Hola! Esta es una notificación de prueba.');
});