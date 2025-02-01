// Obtener el contexto del canvas para el gráfico de ovinos
const ctxOvinos = document.getElementById('myChartOvinos').getContext('2d');
let myChartOvinos;

const stageTypes = ['Lambs', 'Ewe Lambs', 'Yearlings', 'Yearling Ewes', 'Rams', 'Ewes'];

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
                Lambs: data.sheep_count['Lambs'] || 0,
                'Ewe Lambs': data.sheep_count['Ewe Lambs'] || 0,
                Yearlings: data.sheep_count['Yearlings'] || 0,
                'Yearling Ewes': data.sheep_count['Yearling Ewes'] || 0,
                Rams: data.sheep_count['Rams'] || 0,
                Ewes: data.sheep_count['Ewes'] || 0
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
        myChartOvinos.data.datasets[0].data = stageTypes.map(type => cantidadOvinos[type]);
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