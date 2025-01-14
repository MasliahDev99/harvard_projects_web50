// Obtener el contexto del canvas para los gráficos
const ctx = document.getElementById('myChart').getContext('2d');
const ctxOvinos = document.getElementById('myChartOvinos').getContext('2d');
let myChart, myChartOvinos;

const salesTypes = ['Remates', 'Individuales', 'Frigorífico', 'Donaciones'];
const stageTypes = ['Corderas', 'Borregas', 'Corderos', 'Borregos', 'Carnero', 'Oveja'];

// Función para inicializar los gráficos
function initChart() {
    // Inicializamos el gráfico de ventas
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

    // Inicializamos el gráfico de ovinos
    myChartOvinos = new Chart(ctxOvinos, {
        type: 'pie',
        data: {
            labels: stageTypes,
            datasets: [{
                data: [0, 0, 0, 0, 0, 0],
                backgroundColor: ['#28a745', '#218838', '#ffc107', '#dc3545', '#17a2b8', '#6c757d'],  // Nuevos colores
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

// Función para obtener los datos del servidor y actualizar ambas gráficas
function obtenerDatosServidor() {
    fetch('/api/establecimiento/')
        .then(response => {
            if (!response.ok) throw new Error('Error al cargar los datos del establecimiento.');
            return response.json();
        })
        .then(data => {
            console.log('Datos recibidos:', data); // Para depuración

            let cantidadVentas = {
                Remates: 0,
                Individuales: 0,
                Frigorífico: 0,
                Donaciones: 0
            };
            
            let cantidadOvinos = {
                Corderas: 0,
                Borregas: 0,
                Corderos: 0,
                Borregos: 0,
                Carneros: 0,  
                Ovejas: 0     
            };

            // Procesamos los datos de ventas
            const ventas = data.cantidad_ventas_cat;
            cantidadVentas.Remates = ventas.cantidad_ventas_por_remate || 0;
            cantidadVentas.Individuales = ventas.cantidad_ventas_por_individual || 0;
            cantidadVentas.Frigorífico = ventas.cantidad_ventas_por_frigorifico || 0;
            cantidadVentas.Donaciones = ventas.cantidad_donaciones || 0;

            // Procesamos los datos de ovinos
            const ovinos = data.cantidad_ovinos;
            cantidadOvinos.Corderas = ovinos.Corderas || 0;
            cantidadOvinos.Borregas = ovinos.Borregas || 0;
            cantidadOvinos.Corderos = ovinos.Corderos || 0;
            cantidadOvinos.Borregos = ovinos.Borregos || 0;
            cantidadOvinos.Carneros = ovinos.Carneros || 0;  
            cantidadOvinos.Ovejas = ovinos.Ovejas || 0;

            console.log('Cantidad de ventas:', cantidadVentas); // Para depuración
            console.log('Cantidad de ovinos:', cantidadOvinos); // Para depuración

            // Actualizamos las gráficas
            actualizarGraficaVentas(cantidadVentas);
            actualizarGraficaOvinos(cantidadOvinos);
        })
        .catch(error => console.error('Error al obtener los datos:', error));
}

// Función para actualizar el gráfico de ventas
function actualizarGraficaVentas(cantidadVentas) {
    const noVentasLabel = document.getElementById('noVentasLabel'); // Un elemento HTML para mensajes dinámicos
    // si la cantidad de ventas es 0 entonces mostrar un label 'No hay ventas registradas'
    if (hayVentas(cantidadVentas)){
            noVentasLabel.style.display = 'none';
            myChart.data.datasets[0].data = [
                cantidadVentas.Remates,
                cantidadVentas.Individuales,
                cantidadVentas.Frigorífico,
                cantidadVentas.Donaciones
            ];
            myChart.update();
    }else{
        noVentasLabel.style.display = 'block';
    }
}

// Función para actualizar el gráfico de ovinos
function actualizarGraficaOvinos(cantidadOvinos) {
    const noOvinosLabel = document.getElementById('noOvinosLabel'); // Un elemento HTML para mensajes dinámicos
    if (hayOvinos(cantidadOvinos)){
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
    }else{
        noOvinosLabel.style.display='block';
    }

}


function hayVentas(cantidadVentas){
    // retorna true si encuentra ventas en el diccionario
    for (const ventas in cantidadVentas){
        if (cantidadVentas[ventas] > 0){
            return true
        }
    }
    return false
}
function hayOvinos(cantidadOvinos){
    // retorna true si encuentra ovinos en el diccionario
    for (const ovinos in cantidadOvinos){
        if(cantidadOvinos[ovinos] > 0){
            return true
        }
    }
    return false
}

// Inicializamos los gráficos y cargamos los datos cuando la página esté lista
document.addEventListener('DOMContentLoaded', function () {
    initChart();
    obtenerDatosServidor();
});