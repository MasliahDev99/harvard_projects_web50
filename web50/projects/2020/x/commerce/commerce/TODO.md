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

1.  Crear un `home.html` como pagina home de la aplicacion.
2.  Mejorar la plantilla base `layout.html`.
3. `index.html` quedara como plantilla para mostrar las subastas activas
4.  Crear una pagina para mostrar todas las subastas finalizadas `Closed listings`.
5.  Crear una pagina que muestre el historial de todas las subastas que el usuario participo, mostrando en 🟩 las subastas ganadoras y en 🟥 las perdidas.
6. Implementar completamente el sistema de ofertas a las subastas. Cuando la fecha de finalizacion llega a su fin, mostrar en la tarjeta de la subasta  `El usuario 'username' ha sido el ganador` y la subasta queda inactiva.
7. `refactorizas y testear`.
8. `Grabar la app `.