document.addEventListener('DOMContentLoaded', function() {
    // Capturamos todas las filas con la clase "ovino_row"
    const rows = document.querySelectorAll('.ovino_row');

    // Añadimos un event listener a cada fila
    rows.forEach(function(row) {
        row.addEventListener('click', function(event) {

            const isButtonClicked = event.target.closest('a');
            
            // Si el clic fue en el botón "ver detalle", no ejecutamos el evento de la fila
            if (isButtonClicked) {
                return;
            }

            // Obtenemos el id de la fila seleccionada
            const id = row.getAttribute('data-id');
            // Mostramos el id con un alert
            alert(`El id del ovino seleccionado es: ${id}`);

            // enviamos el id al servidor backend

            
            
        });
    });
});



document.addEventListener('DOMContentLoaded', function() {
    const obsCheckbox = document.getElementById('obs');
    const observacionesContainer = document.getElementById('observacionesContainer');
    const purchasedCheckbox = document.getElementById('purchased');
    const purchasedHidden = document.querySelectorAll('.purchased-hidden');
    const purchasedVisible = document.querySelectorAll('.purchased-visible');

    obsCheckbox.addEventListener('change', function() {
        observacionesContainer.style.display = this.checked ? 'block' : 'none';
    });

    purchasedCheckbox.addEventListener('change', function() {
        const isChecked = this.checked;
        purchasedHidden.forEach(field => {
            field.style.display = isChecked ? 'none' : 'block';
        });
        purchasedVisible.forEach(field => {
            field.style.display = isChecked ? 'block' : 'none';
        });
    });

    // Validación del formulario
    const addOvinoForm = document.getElementById('addOvinoForm');
    addOvinoForm.addEventListener('submit', function(event) {
        if (!addOvinoForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        addOvinoForm.classList.add('was-validated');
    });
});