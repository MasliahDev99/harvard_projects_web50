// Obtener el contexto del canvas para el gráfico de ovinos
const ctxOvinos = document.getElementById('myChartOvinos').getContext('2d');
let myChartOvinos;

const stageTypes = ['Corderas', 'Borregas', 'Corderos', 'Borregos', 'Carneros', 'Ovejas'];

// Función para inicializar el gráfico de ovinos
function initOvinosChart() {
    myChartOvinos = new Chart(ctxOvinos, {
        type: 'pie',
        data: {
            labels: stageTypes,
            datasets: [{
                data: [0, 0, 0, 0, 0, 0],
                backgroundColor: ['#28a745', '#218838', '#ffc107', '#dc3545', '#17a2b8', '#6c757d'],
                borderColor: ['#28a745', '#218838', '#ffc107', '#dc3545', '#17a2b8', '#6c757d'],
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

// Función para obtener los datos de ovinos del servidor
function obtenerDatosOvinos() {
    fetch('/api/establecimiento/')
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar los datos del establecimiento.');
            return response.json();
        })
        .then(data => {
            console.log('Datos de ovinos recibidos:', data); // Para depuración

            let cantidadOvinos = {
                Corderas: data.cantidad_ovinos.Corderas || 0,
                Borregas: data.cantidad_ovinos.Borregas || 0,
                Corderos: data.cantidad_ovinos.Corderos || 0,
                Borregos: data.cantidad_ovinos.Borregos || 0,
                Carneros: data.cantidad_ovinos.Carneros || 0,
                Ovejas: data.cantidad_ovinos.Ovejas || 0
            };

            console.log('Cantidad de ovinos:', cantidadOvinos); // Para depuración

            // Actualizamos la gráfica
            actualizarGraficaOvinos(cantidadOvinos);
        })
        .catch(error => {
            console.error('Error al obtener los datos de ovinos:', error);
            mostrarMensajeError();
        });
}

// Función para actualizar el gráfico de ovinos
function actualizarGraficaOvinos(cantidadOvinos) {
    const noOvinosLabel = document.getElementById('noOvinosDistribucionLabel');
    if (hayOvinos(cantidadOvinos)) {
        noOvinosLabel.style.display = 'none';
        myChartOvinos.data.datasets[0].data = [
            cantidadOvinos.Corderas,
            cantidadOvinos.Borregas,
            cantidadOvinos.Corderos,
            cantidadOvinos.Borregos,
            cantidadOvinos.Carneros, 
            cantidadOvinos.Ovejas     
        ];
        myChartOvinos.update();
    } else {
        noOvinosLabel.style.display = 'block';
        myChartOvinos.data.datasets[0].data = [0, 0, 0, 0, 0, 0];
        myChartOvinos.update();
    }
}

function hayOvinos(cantidadOvinos) {
    return Object.values(cantidadOvinos).some(cantidad => cantidad > 0);
}

function mostrarMensajeError() {
    const noOvinosLabel = document.getElementById('noOvinosDistribucionLabel');
    noOvinosLabel.textContent = 'Error al cargar los datos de ovinos.';
    noOvinosLabel.style.display = 'block';
}

// Inicializamos el gráfico y cargamos los datos cuando la página esté lista
document.addEventListener('DOMContentLoaded', function () {
    initOvinosChart();
    obtenerDatosOvinos();
});

