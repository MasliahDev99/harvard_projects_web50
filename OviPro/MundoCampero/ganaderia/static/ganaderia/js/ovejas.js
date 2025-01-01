document.addEventListener('DOMContentLoaded', function() {
    // Capturamos todas las filas con la clase "ovino_row"
    const rows = document.querySelectorAll('.ovino_row');

    // Añadimos un event listener a cada fila
    rows.forEach(function(row) {
        row.addEventListener('click', function() {
            // Obtenemos el id de la fila seleccionada
            const id = row.getAttribute('data-id');
            // Mostramos el id con un alert
            alert(`El id del ovino seleccionado es: ${id}`);
            
        });
    });
});