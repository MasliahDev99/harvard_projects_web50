



document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
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

  



    // Array para almacenar los ovinos disponibles
    let ovinosDisponibles = [];

    // Obtener los ovinos disponibles desde el servidor
    function obtenerOvinosServidor() {
        fetch('/api/ovejas/')
            .then(response => {
                if (!response.ok) throw new Error('Error al cargar la lista de animales.');
                return response.json();
            })
            .then(data => {
                // Ordenar los ovinos por RP
                ovinosDisponibles = data.sort((a, b) => a.RP.localeCompare(b.RP, undefined, {numeric: true}));
                cargarOvinos();
            })
            .catch(error => console.error('Error:', error));
    }

    // Cargar los ovinos en el select
    function cargarOvinos() {
        animalSelect.innerHTML = '';
        const fragment = document.createDocumentFragment();
        ovinosDisponibles.forEach(ovino => {
            const option = new Option(`RP: ${ovino.RP} - ${ovino.peso} kg`, ovino.RP);
            fragment.appendChild(option);
        });
        animalSelect.appendChild(fragment);
    }

    // Llamar a la función para obtener los ovinos al cargar la página
    obtenerOvinosServidor();

    // Event Listeners
    saleType.addEventListener('change', updateFormFields);
    batchSale.addEventListener('change', updateAnimalSelection);
    animalSelect.addEventListener('change', updateSelectedAnimals);
    pricePerKg.addEventListener('input', calculateFrigorificoTotal);
    remateTotal.addEventListener('input', updateTotalSaleValue);
    confirmSaleBtn.addEventListener('click', submitSaleForm);

    // Actualizar los campos del formulario según el tipo de venta
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

    // Actualizar la selección de animales
    function updateAnimalSelection() {
        animalSelect.multiple = !batchSale.checked;
        if (batchSale.checked) {
            Array.from(animalSelect.selectedOptions).slice(10).forEach(option => option.selected = false);
        }
        updateSelectedAnimals();
    }

    // Actualizar la lista de animales seleccionados
    function updateSelectedAnimals() {
        selectedAnimals.innerHTML = '';
        let totalWeightValue = 0;
        
        Array.from(animalSelect.options).forEach(option => {
            const animal = ovinosDisponibles.find(a => a.RP === option.value);
            if (option.selected) {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.textContent = `RP: ${animal.RP} - ${animal.peso} kg`;

                if (saleType.value === 'individual') {
                    const input = document.createElement('input');
                    input.type = 'number';
                    input.className = 'form-control form-control-sm w-25';
                    input.placeholder = 'Precio';
                    input.addEventListener('input', calculateIndividualTotal);
                    li.appendChild(input);
                }
                
                selectedAnimals.appendChild(li);
                totalWeightValue += animal.peso;
                option.style.color = 'green';
            } else {
                option.style.color = '';
            }
        });

        totalWeight.value = totalWeightValue.toFixed(2);
        calculateFrigorificoTotal();
    }

    // Calcular el total para venta a frigorífico
    function calculateFrigorificoTotal() {
        if (saleType.value === 'frigorifico') {
            const total = (parseFloat(totalWeight.value) || 0) * (parseFloat(pricePerKg.value) || 0);
            totalSaleValue.value = total.toFixed(2);
        }
    }

    // Calcular el total para ventas individuales
    function calculateIndividualTotal() {
        if (saleType.value === 'individual') {
            let total = 0;
            selectedAnimals.querySelectorAll('input').forEach(input => {
                total += parseFloat(input.value) || 0;
            });
            totalSaleValue.value = total.toFixed(2);
        }
    }

    // Actualizar el valor total de la venta en el caso de remate
    function updateTotalSaleValue() {
        if (saleType.value === 'remate') {
            totalSaleValue.value = remateTotal.value;
        }
    }

    // Enviar el formulario de venta al servidor para registrar la venta
    function submitSaleForm(event) {
        event.preventDefault();
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    
        // URL para enviar los datos al servidor
        URL = window.location.origin+'/hub/dashboard/ventas/'
        console.log("La url del fetch es: ",URL)
        fetch(URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({
                tipo_venta: saleType.value,
                por_lote: batchSale.checked,
                ovinos: Array.from(animalSelect.selectedOptions).map(o => o.value),
                peso_total: totalWeight.value,
                precio_kg: pricePerKg.value,
                remate_total: remateTotal.value,
                fecha_venta: saleDate.value,
                valor_total: totalSaleValue.value,
            })
            
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            if(data.success){
                //si fue un exito refresca la pagina
                window.location.reload();
            }else{
                console.error('Error en el registro de la venta:', data.message);
            }
        })
        .catch(error => console.error('Error:', error))




        bootstrap.Modal.getInstance(document.getElementById('addSaleModal')).hide();
        document.getElementById('addSaleForm').reset();
    }
});