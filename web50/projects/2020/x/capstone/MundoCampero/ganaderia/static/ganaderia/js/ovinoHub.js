document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('lastUpdate').textContent = new Date().toLocaleString();

    const form = document.getElementById('priceCalculator');
    const weightInput = document.getElementById('weight');
    const animalTypeSelect = document.getElementById('animalType');
    const butcherSelect = document.getElementById('butcher');
    const resultDiv = document.getElementById('result');
    const estimatedPriceSpan = document.getElementById('estimatedPrice');

    const prices = {
        canelo: { cordero: 4.18, carnero: 3.98 },
        pepito: { cordero: 4.15, carnero: 3.98 }
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        calculatePrice();
    });

    function calculatePrice() {
        const weight = parseFloat(weightInput.value);
        const animalType = animalTypeSelect.value;
        const butcher = butcherSelect.value;

        if (weight && animalType && butcher) {
            const pricePerKg = prices[butcher][animalType];
            const totalPrice = pricePerKg * weight;

            resultDiv.style.display = 'block';
            estimatedPriceSpan.textContent = totalPrice.toFixed(2);
            
            // Add animation
            resultDiv.classList.add('animate__animated', 'animate__fadeIn');
        }
    }
});