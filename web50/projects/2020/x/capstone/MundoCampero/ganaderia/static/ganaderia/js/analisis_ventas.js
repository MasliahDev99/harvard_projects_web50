// Obtener el contexto del canvas para el gráfico de ventas
const ctx = document.getElementById('myChart').getContext('2d');
let myChart;

const salesTypes = ['Auctions', 'Individuals', 'Slaughterhouse', 'Donations'];

// Función para inicializar el gráfico de ventas
function initVentasChart() {
    myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: salesTypes,
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: ['#28a745', '#ffc107', '#dc3545', '#007bff'],
                borderColor: ['#28a745', '#ffc107', '#dc3545', '#007bff'],
                borderWidth: 1,
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                tooltip: { enabled: true }
            }
        }
    });
}

// Función para obtener los datos de ventas del servidor
function obtenerDatosVentas() {
    fetch('/api/establecimiento/')
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar los datos del establecimiento.');
            return response.json();
        })
        .then(data => {
            console.log('Datos de ventas recibidos:', data); // Para depuración

            let salesCount = {
                Auctions: data.sale_category_count.auction_sales_count|| 0,
                Individuals: data.sale_category_count.individual_sales_count || 0,
                Slaughterhouse: data.sale_category_count.slaughterhouse_sales_count || 0,
                Donations: data.sale_category_count.donation_count || 0
            };

            console.log('Cantidad de ventas:', salesCount); // Para depuración

            // Actualizamos la gráfica
            actualizarGraficaVentas(salesCount);
        })
        .catch(error => {
            console.error('Error al obtener los datos de ventas:', error);
            mostrarMensajeError();
        });
}

// Función para actualizar el gráfico de ventas
function actualizarGraficaVentas(salesCount) {
    const noVentasLabel = document.getElementById('noVentasLabel');
    if (hayVentas(salesCount)) {
        noVentasLabel.style.display = 'none';
        myChart.data.datasets[0].data = [
            salesCount.Auctions,
            salesCount.Individuals,
            salesCount.Slaughterhouse,
            salesCount.Donations
        ];
        myChart.update();
    } else {
        noVentasLabel.style.display = 'block';
        myChart.data.datasets[0].data = [0, 0, 0, 0];
        myChart.update();
    }
}

function hayVentas(salesCount) {
    return Object.values(salesCount).some(count => count > 0);
}

function mostrarMensajeError() {
    const noVentasLabel = document.getElementById('noVentasLabel');
    noVentasLabel.textContent = 'Error al cargar los datos de ventas.';
    noVentasLabel.style.display = 'block';
}

// Inicializamos el gráfico y cargamos los datos cuando la página esté lista
document.addEventListener('DOMContentLoaded', function () {
    initVentasChart();
    obtenerDatosVentas();
});

