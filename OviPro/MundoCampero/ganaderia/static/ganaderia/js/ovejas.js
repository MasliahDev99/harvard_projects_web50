document.addEventListener('DOMContentLoaded', function() {
    const obsCheckbox = document.getElementById('obs');
    const observacionesContainer = document.getElementById('observacionesContainer');
    const purchasedCheckbox = document.getElementById('purchased');
    const purchasedHidden = document.querySelectorAll('.purchased-hidden');
    const purchasedVisible = document.querySelectorAll('.purchased-visible');
    const calificadorPurezaSelect = document.getElementById('calificador_pureza');
    const purchasedSection = document.querySelector('.purchased-hidden');
    const rpPadreSection = document.querySelectorAll('.purchased-hidden');
    const rpMadreSection = document.querySelectorAll('.purchased-hidden');

    // Muestra las observaciones si el checkbox es activado
    obsCheckbox.addEventListener('change', function() {
        observacionesContainer.style.display = this.checked ? 'block' : 'none';
    });

    // Muestra/oculta los campos de acuerdo con "¿Oveja comprada?"
    purchasedCheckbox.addEventListener('change', function() {
        const isChecked = this.checked;
        purchasedHidden.forEach(field => {
            field.style.display = isChecked ? 'none' : 'block';
        });
        purchasedVisible.forEach(field => {
            field.style.display = isChecked ? 'block' : 'none';
        });
    });

    // Muestra los campos "RP padre" y "RP madre" si el calificador de pureza es "pedigree" o "pedigrí"
    calificadorPurezaSelect.addEventListener('change', function() {
        const selectedValue = this.value.toLowerCase();
        if (selectedValue === "pedigree" || selectedValue === "pedigrí") {
            rpPadreSection.forEach(field => field.style.display = 'block');
            rpMadreSection.forEach(field => field.style.display = 'block');
            purchasedSection.forEach(field => field.style.display = 'block');
        } else {
            rpPadreSection.forEach(field => field.style.display = 'none');
            rpMadreSection.forEach(field => field.style.display = 'none');
            purchasedSection.forEach(field => field.style.display = 'none');
        }
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