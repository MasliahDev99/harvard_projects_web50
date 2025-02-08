# TODO ✅

### Bugs 🚩

* Cuando un usuario guarda en favoritos/watchlist una subasta el boton queda en estado de 'remove' para todos los usuarios, aunque no los tengan en favoritos.
    *   ### Solucion:
        * Obtener las subastas agregadas a lista de seguimiento filtradas por usuario logeado, con eso el estado del boton 'watch/remove' no queda fijo en todos los usuarios
        * Arreglar el metodo `get_auctions_by` para que unicamente se encargue de retornar todas las subastas por cualquier parametro `**kwargs` 

        * Implementar un metedo para que se encargue de obtener todas las subastas  agregadas a la lista de seguimiento del usuario logeado.
        `get_user_watchlist`.

        # Solucionado ✅
          *  ### Backend:
                utils.py
                ```python
                    def get_user_watchlist_auctions(user, **kwargs):
                        return Auction.objects.filtr(
                            watchlist__user=user,
                            **kwargs,
                        ).prefetch_related
                        (
                        Prefetch('watchlisted_by',queryset=Watchlist.objects.filter(user=user),to_attr='user_watchlist'))
                ```
          *  ### Frontend:
                auctions.html
                ```Django
                    {% if auctions in auctions_watchlisted %}
                        <i class="fas fa-heart me-1"></i>Remove
                    {% else %}
                        <i class="far fa-heart me-1"></i>Watch
                    {% endif %}
                ```
                
* En `Categories.html`  donde se muestran todas las categorias existentes y la cantidad de subastas que hay en cada categoria deberia mostrar el numero de subastas activas y no el  total  que existen en dicha categoria, filtramos en `active listings` las subastas activas hay subastas desactivadas que no estan eliminadas del sistema por ende las cuenta. 
    * ### Solucion:
        * Obtener la cantidad de subastas `ACTIVAS` por categoria.
        * Generar una `API` local y consumirla en el front para actualizar datos del backend en el front de una manera mas simple. Para este proyecto no es necesario.

        # Solucionado ✅
            
---

### Para implementar 🔧 y gestionar ⚙️

1.  Implementar el sistema de eliminar y editar comentarios
2.  Analizar el uso de la api en la app
3.  Arreglar el redireccionamiento en bucle  al regresar de pagina cuando se refresca la pagina.
4.  Arreglar el sistema de paginacion en el front.
5. pulir las subastas mostradas cuando hay un ganador y actualizar el progreso en bid history

6. refactorizar y eliminar redundancias
7. documentar
8. grabar y aprontar.





## Documentación sobre la API 📖 

### Estructura

- **auctions/api/serializers.py**: Define los serializadores para los modelos de subastas y ofertas, permitiendo la conversión de instancias de modelo a JSON y viceversa.
- **auctions/api/views.py**: Contiene las vistas de la API que manejan las solicitudes HTTP para las subastas y ofertas, utilizando los serializadores para procesar los datos.
- **auctions/api/urls.py**: Define las rutas de la API, mapeando las URL a las vistas correspondientes.

### Posibles Usos

- **Gestión de Subastas**: Permite crear, leer, actualizar y eliminar subastas a través de solicitudes HTTP, facilitando la gestión de subastas desde aplicaciones externas o interfaces de usuario personalizadas.
- **Seguimiento de Ofertas**: Proporciona un mecanismo para rastrear las ofertas realizadas en cada subasta, permitiendo a los usuarios ver el historial de ofertas y el estado actual de cada subasta.

### Uso Planificado

- **Actualización en Tiempo de Ejecución**: Utilizaré la API para verificar periódicamente las subastas que están por llegar a su fecha de finalización. Al detectar que una subasta ha terminado, enviaré una solicitud para actualizar su estado.
- **Determinación del Ganador**: Una vez que una subasta finaliza, la API se utilizará para determinar el ganador basado en la oferta más alta. Si hay un ganador, se enviará un mensaje al front-end para mostrar "El ganador es ...". Si no hubo ofertas, se mostrará "La subasta no tuvo ofertas, cerrada...".






### Ejemplo de Uso

- **Obtener Todas las Subastas**:
  ```bash
  curl http://localhost:8000/api/auctions/

* Crear una nueva subasta
  ```bash
    curl -X POST http://localhost:8000/api/auctions/ \
    -H "Authorization: Token YOUR_AUTH_TOKEN" \
    -H "Content-Type: multipart/form-data" \
    -F "title=Sample Auction" \
    -F "description=This is a sample auction" \
    -F "starting_bid=100.00" \
    -F "end_date=2023-12-31" \
    -F "end_time=23:59:59" \
    -F "image=@/path/to/image.jpg"
  ```




