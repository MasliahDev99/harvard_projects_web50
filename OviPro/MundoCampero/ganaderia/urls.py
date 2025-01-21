from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ganaderia'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),

    #URLS HUB  
    path('hub/', views.hub, name='hub'),

    # URLS de dashboard
    path('hub/dashboard/', views.dashboard, name='dashboard'),
    path('hub/dashboard/ventas/', views.ventas, name='ventas'),
    path('hub/dashboard/ventas/detalle/<int:id_venta>',views.detalle_venta,name='ver_detalle_venta'),
    
    path('hub/dashboard/ovejas/', views.ovejas, name='ovejas'),
    # URLS para ver el detalle de la oveja con id_oveja = id
    path('hub/dashboard/oveja/detalle/<int:id_oveja>/', views.ver_detalle, name='ver_detalle'),
    path('hub/dashboard/ovejas/detalle/eliminar/<int:id_oveja>/',views.eliminar_oveja,name='eliminar_oveja'),
    path('hub/dashboard/ovejas/detalle/editar/<int:id_oveja>/',views.editar_oveja,name="editar_ovino"),

    #descarga de tabla
    path('hub/dashboard/ovejas/descarga/',views.descargar_tabla,name='tabla_registro'),

    path('hub/dashboard/planteletas/', views.planteletas, name='planteletas'),

    # dashboard analisis de datos
    path('hub/dashboard/analisis/ventas/', views.analisis_ventas, name='analisis_ventas'),
path('hub/dashboard/analisis/ovinos/', views.analisis_ovinos, name='analisis_ovinos'),

    # API View
    path('api/ovejas/',views.OvejaListadoAPI.as_view(),name='OvinoApi'),
    path('api/establecimiento/',views.EstablecimientoAPI.as_view(),name='Establecimiento'),
    path('api/ventas/',views.VentaListadoAPI.as_view(),name='Venta'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
