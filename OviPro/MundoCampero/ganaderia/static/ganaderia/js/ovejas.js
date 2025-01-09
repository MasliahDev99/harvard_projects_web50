document.addEventListener('DOMContentLoaded', function() {
    const obsCheckbox = document.getElementById('obs');
    const observacionesContainer = document.getElementById('observacionesContainer');
    const purchasedCheckbox = document.getElementById('purchased');
    const purchasedHidden = document.querySelectorAll('.purchased-hidden');
    const purchasedVisible = document.querySelectorAll('.purchased-visible');
    const calificadorPurezaSelect = document.getElementById('calificador_pureza');
    const parentSection = document.getElementById('parentSection');

    function toggleParentFields() {
        const selectedValue = calificadorPurezaSelect.value.toLowerCase();
        const isPedigree = selectedValue === "pedigree" || selectedValue === "pedigri";
        
        parentSection.style.display = isPedigree ? 'block' : 'none';
        
        if (isPedigree) {
            togglePurchasedFields();
        } else {
            purchasedHidden.forEach(field => {
                if (field !== purchasedCheckbox.parentElement.parentElement) {
                    field.style.display = 'none';
                }
            });
            purchasedVisible.forEach(field => field.style.display = 'none');
        }

        // Always show the "oveja comprada" checkbox
        purchasedCheckbox.parentElement.parentElement.style.display = 'block';
    }

    function togglePurchasedFields() {
        const isChecked = purchasedCheckbox.checked;
        purchasedHidden.forEach(field => {
            if (field !== purchasedCheckbox.parentElement.parentElement) {
                field.style.display = isChecked ? 'none' : 'block';
            }
        });
        purchasedVisible.forEach(field => field.style.display = isChecked ? 'block' : 'none');
    }

    // Muestra las observaciones si el checkbox es activado
    obsCheckbox.addEventListener('change', function() {
        observacionesContainer.style.display = this.checked ? 'block' : 'none';
    });

    // Maneja los cambios en el checkbox de "¿Oveja comprada?"
    purchasedCheckbox.addEventListener('change', togglePurchasedFields);

    // Maneja los cambios en el select de calificador de pureza
    calificadorPurezaSelect.addEventListener('change', toggleParentFields);

    // Configuración inicial
    toggleParentFields();
    observacionesContainer.style.display = 'none';

    // Ensure the checkbox is visible on page load
    purchasedCheckbox.parentElement.parentElement.style.display = 'block';

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