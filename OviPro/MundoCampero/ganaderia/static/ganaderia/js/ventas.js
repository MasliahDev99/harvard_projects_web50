document.addEventListener('DOMContentLoaded', function() {
    const saleType = document.getElementById('saleType');
    const batchSale = document.getElementById('batchSale');
    const animalSelect = document.getElementById('animalSelect');
    const selectedAnimals = document.getElementById('selectedAnimals');
    const frigorificoFields = document.getElementById('frigorificoFields');
    const remateFields = document.getElementById('remateFields');
    const individualFields = document.getElementById('individualFields');
    const totalWeight = document.getElementById('totalWeight');
    const pricePerKg = document.getElementById('pricePerKg');
    const remateTotal = document.getElementById('remateTotal');
    const totalSaleValue = document.getElementById('totalSaleValue');
    const confirmSaleBtn = document.getElementById('confirmSale');
    const finalConfirmSaleBtn = document.getElementById('finalConfirmSale');

    // Mock data for available animals
    const availableAnimals = [
        { rp: 'RP001', weight: 50 },
        { rp: 'RP002', weight: 55 },
        { rp: 'RP003', weight: 48 },
        { rp: 'RP004', weight: 52 },
        { rp: 'RP005', weight: 58 },
        // Add more animals as needed
    ];

    // Populate animal select options
    availableAnimals.forEach(animal => {
        const option = new Option(animal.rp, animal.rp);
        animalSelect.add(option);
    });

    saleType.addEventListener('change', updateFormFields);
    batchSale.addEventListener('change', updateAnimalSelection);
    animalSelect.addEventListener('change', updateSelectedAnimals);
    pricePerKg.addEventListener('input', calculateFrigorificoTotal);
    remateTotal.addEventListener('input', updateTotalSaleValue);
    confirmSaleBtn.addEventListener('click', showConfirmation);
    finalConfirmSaleBtn.addEventListener('click', submitSaleForm);

    function updateFormFields() {
        frigorificoFields.style.display = saleType.value === 'frigorifico' ? 'block' : 'none';
        remateFields.style.display = saleType.value === 'remate' ? 'block' : 'none';
        individualFields.style.display = saleType.value === 'individual' ? 'block' : 'none';
        
        if (saleType.value === 'donacion') {
            totalSaleValue.value = '0';
        }
        
        updateAnimalSelection();
        updateSelectedAnimals();
    }

    function updateAnimalSelection() {
        animalSelect.multiple = !batchSale.checked;
        if (batchSale.checked) {
            Array.from(animalSelect.selectedOptions).slice(10).forEach(option => option.selected = false);
        }
    }

    function updateSelectedAnimals() {
        selectedAnimals.innerHTML = '';
        let totalWeightValue = 0;
        
        Array.from(animalSelect.selectedOptions).forEach(option => {
            const animal = availableAnimals.find(a => a.rp === option.value);
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.textContent = animal.rp;
            
            if (saleType.value === 'individual') {
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'form-control form-control-sm w-25';
                input.placeholder = 'Precio';
                input.addEventListener('input', calculateIndividualTotal);
                li.appendChild(input);
            }
            
            selectedAnimals.appendChild(li);
            totalWeightValue += animal.weight;
            option.style.color = 'green';
        });

        availableAnimals.forEach(animal => {
            const option = animalSelect.querySelector(`option[value="${animal.rp}"]`);
            if (!option.selected) {
                option.style.color = '';
            }
        });

        totalWeight.value = totalWeightValue;
        calculateFrigorificoTotal();
    }

    function calculateFrigorificoTotal() {
        if (saleType.value === 'frigorifico') {
            const total = (parseFloat(totalWeight.value) || 0) * (parseFloat(pricePerKg.value) || 0);
            totalSaleValue.value = total.toFixed(2);
        }
    }

    function calculateIndividualTotal() {
        if (saleType.value === 'individual') {
            let total = 0;
            selectedAnimals.querySelectorAll('input').forEach(input => {
                total += parseFloat(input.value) || 0;
            });
            totalSaleValue.value = total.toFixed(2);
        }
    }

    function updateTotalSaleValue() {
        if (saleType.value === 'remate') {
            totalSaleValue.value = remateTotal.value;
        }
    }

    function showConfirmation() {
        const saleDetails = document.getElementById('saleDetails');
        let detailsHTML = `
            <p><strong>Tipo de Venta:</strong> ${saleType.options[saleType.selectedIndex].text}</p>
            <p><strong>Fecha de Venta:</strong> ${document.getElementById('saleDate').value}</p>
            <p><strong>Valor Total:</strong> $${totalSaleValue.value}</p>
            <p><strong>Animales Vendidos:</strong></p>
            <ul>
        `;

        Array.from(animalSelect.selectedOptions).forEach(option => {
            detailsHTML += `<li>${option.text}</li>`;
        });

        detailsHTML += '</ul>';

        if (saleType.value === 'frigorifico') {
            detailsHTML += `
                <p><strong>Peso Total:</strong> ${totalWeight.value} kg</p>
                <p><strong>Precio por kg:</strong> $${pricePerKg.value}</p>
            `;
        }

        saleDetails.innerHTML = detailsHTML;
        const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));
        confirmationModal.show();
    }

    function submitSaleForm() {
        // Here you would typically send the form data to your server
        console.log('Sale form submitted', {
            type: saleType.value,
            animals: Array.from(animalSelect.selectedOptions).map(o => o.value),
            totalValue: totalSaleValue.value,
            date: document.getElementById('saleDate').value
        });
        // Close both modals
        bootstrap.Modal.getInstance(document.getElementById('confirmationModal')).hide();
        bootstrap.Modal.getInstance(document.getElementById('addSaleModal')).hide();
        // Reset the form
        document.getElementById('addSaleForm').reset();
    }
});
