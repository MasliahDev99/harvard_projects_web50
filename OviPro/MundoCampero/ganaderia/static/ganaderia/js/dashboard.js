 // Obtener el contexto del canvas
 var ctx = document.getElementById('myChart').getContext('2d');

 // Crear la gráfica de torta (pie chart)
 var myChart = new Chart(ctx, {
     type: 'pie', // Tipo de gráfico: 'pie' para gráfica de torta
     data: {
         labels: ['Remates', 'Individuales', 'Frigorífico'], // Etiquetas para las categorías
         datasets: [{
             data: [70, 10, 20], // Datos de las ventas por cada categoría
             backgroundColor: ['#28a745', '#ffc107', '#dc3545'], // Colores: verde, amarillo, rojo
             borderColor: ['#28a745', '#ffc107', '#dc3545'], // Colores del borde (opcional)
             borderWidth: 1, // Grosor del borde
         }]
     },
     options: {
         responsive: true, // Para hacerlo adaptable al tamaño de la pantalla
         plugins: {
             legend: {
                 position: 'top', // Posición de la leyenda
             },
             tooltip: {
                 enabled: true // Habilitar los tooltips al pasar el mouse
             }
         }
     }
 });
 // Obtener el contexto del canvas
var ctxOvinos = document.getElementById('myChartOvinos').getContext('2d');

// Crear la gráfica de torta (pie chart)
var myChartOvinos = new Chart(ctxOvinos, {
 type: 'pie', // Tipo de gráfico: 'pie' para gráfica de torta
 data: {
     labels: ['Corderas', 'Borregas', 'Corderos', 'Borregos'], // Etiquetas de las categorías
     datasets: [{
         data: [50, 30, 40, 20], // Datos para cada categoría (actualiza con tus valores reales)
         backgroundColor: ['#28a745', '#218838', '#ffc107', '#dc3545'], // Colores: verde, verde oscuro, amarillo, rojo
         borderColor: ['#28a745', '#218838', '#ffc107', '#dc3545'], // Bordes (opcional)
         borderWidth: 1, // Grosor del borde
     }]
 },
 options: {
     responsive: true, // Adaptable al tamaño de la pantalla
     plugins: {
         legend: {
             position: 'top', // Posición de la leyenda
         },
         tooltip: {
             enabled: true // Habilitar los tooltips al pasar el mouse
         }
     }
 }
});