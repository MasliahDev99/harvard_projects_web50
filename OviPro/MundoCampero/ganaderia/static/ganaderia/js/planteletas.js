document.addEventListener('DOMContentLoaded', function() {
    const plantelTypeRadios = document.querySelectorAll('input[name="plantelType"]');
    const exposicionFields = document.getElementById('exposicionFields');
    const ventaFields = document.getElementById('ventaFields');

    plantelTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'exposicion') {
                exposicionFields.style.display = 'block';
                ventaFields.style.display = 'none';
            } else {
                exposicionFields.style.display = 'none';
                ventaFields.style.display = 'block';
            }
        });
    });

    document.getElementById('addSheepForm').addEventListener('submit', function(e) {
        e.preventDefault();
        // Aquí puedes agregar la lógica para procesar el formulario
        console.log('Formulario enviado');
        // Cierra el modal después de procesar
        var modal = bootstrap.Modal.getInstance(document.getElementById('addSheepModal'));
        modal.hide();
    });
});