document.addEventListener('DOMContentLoaded', function() {
    const obsCheckbox = document.getElementById('obs');
    const observacionesContainer = document.getElementById('observacionesContainer');
    const purchasedCheckbox = document.getElementById('purchased');
    const calificadorPurezaSelect = document.getElementById('calificador_pureza');
    const parentSection = document.getElementById('parentSection');
    const purchasedCheckboxContainer = document.getElementById('purchasedCheckboxContainer');
    const origenContainer = document.getElementById('origenContainer');
    const ovejaPadreInput = document.getElementById('oveja_padre');
    const ovejaMadreInput = document.getElementById('oveja_madre');

    function toggleParentFields() {
        const selectedValue = calificadorPurezaSelect.value.toLowerCase();
        const isPedigree = selectedValue === "pedigree" || selectedValue === "pedigri";
        
        parentSection.style.display = isPedigree ? 'block' : 'none';
        purchasedCheckboxContainer.style.display = selectedValue ? 'block' : 'none';
        
        if (!isPedigree) {
            origenContainer.style.display = 'none';
            purchasedCheckbox.checked = false;
        }
        
        togglePurchasedFields();
        updateRequiredFields(isPedigree);
    }

    function togglePurchasedFields() {
        const isChecked = purchasedCheckbox.checked;
        origenContainer.style.display = isChecked ? 'block' : 'none';
    }

    function updateRequiredFields(isPedigree) {
        if (isPedigree) {
            ovejaPadreInput.required = true;
            ovejaMadreInput.required = true;
        } else {
            ovejaPadreInput.required = false;
            ovejaMadreInput.required = false;
        }
    }

    obsCheckbox.addEventListener('change', function() {
        observacionesContainer.style.display = this.checked ? 'block' : 'none';
    });

    purchasedCheckbox.addEventListener('change', togglePurchasedFields);

    calificadorPurezaSelect.addEventListener('change', toggleParentFields);

    // Initial setup
    toggleParentFields();
    observacionesContainer.style.display = 'none';

    // Form validation
    const addOvinoForm = document.getElementById('addOvinoForm');
    addOvinoForm.addEventListener('submit', function(event) {
        const isPedigree = calificadorPurezaSelect.value.toLowerCase() === "pedigree" || calificadorPurezaSelect.value.toLowerCase() === "pedigri";
        
        if (isPedigree) {
            if (!ovejaPadreInput.value || !ovejaMadreInput.value) {
                event.preventDefault();
                alert('Para ovejas pedigri, los campos RP padre y RP madre son obligatorios.');
                return;
            }
        }

        if (!addOvinoForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        addOvinoForm.classList.add('was-validated');
    });
});

