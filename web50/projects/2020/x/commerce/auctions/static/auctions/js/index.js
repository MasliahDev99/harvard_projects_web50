document.addEventListener('DOMContentLoaded', function() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(modal => {
        modal.addEventListener('show.bs.modal', function() {
            const descriptions = this.querySelectorAll('.collapse');
            descriptions.forEach(description => {
                description.classList.remove('show');
            });
        });
    });

    // Script para actualizar en tiempo de ejecucion las fechas de finalizacion de las subastas
    //  consumo los datos de la api de las subastas de la aplicacion

   // creamos una variable para almacenar la fecha y hora actual
   const now = new Date();



    fetch('/api/auctions/')
    .then(response => response.json())
    .then(data => {
        data.forEach(auction => {
            // si la subasta esta activa entonces muestro las subastas
            if(auction.is_active){
                console.log('Auction: ' + auction.title + ' Ends on: ' + auction.end_date + ' at ' + auction.end_time);
            alert('Subasta activa'+'\nAuction: ' + auction.title + ' Ends on: ' + auction.end_date + ' at ' + auction.end_time);
                
            // almacenamos la fecha y hora que termina la subasta activa
            const endDate = new Date(`${auction.end_date}T${auction.end_time}`);
            // calculamos la diferencia de tiempo entre la fecha y hora actual y la fecha y hora que termina la subasta
            const timeRemaining = endDate - now;
            // si la diferencia de tiempo es mayor a 0 entonces muestro la subasta
            if (timeRemaining > 0 ){
                console.log('La Subasta aun no termina'+'\nAuction:'+ auction.title +'Ends on:'+ auction.end_date +'at'+ auction.end_time);
                // si todavia no termino la subasta y la subasta se encuentra en la fecha actual debe mostrar un cronometro del tiempo que queda para terminar la subasta
                // calculamos los dias, horas, minutos y segundos que quedan para terminar la subasta
                const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24));
                const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);
                // mostramos el cronometro
                console.log('La Subasta aun no termina'+'\nAuction:'+ auction.title +'Ends on:'+ auction.end_date +'at'+ auction.end_time +'\nTime remaining: '+ days +'d '+ hours +'h '+ minutes +'m '+ seconds +'s');

            }else{
                console.log('La subasta ya termino'+'\nAuction:'+ auction.title + 'ID' + auction.id + 'has ended.');
            }

            

            }
            
        });
    })
    .catch(error => console.error('Error fetching auction data: ', error));
});