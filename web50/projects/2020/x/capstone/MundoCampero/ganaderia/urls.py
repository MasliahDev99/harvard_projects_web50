from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'ganaderia'


urlpatterns = [
    path('', views.index, name='index'),
    path('about/',views.about,name='about'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),

    #URLS HUB  
    path('hub/', views.hub, name='hub'),

    # URLS de dashboard
    path('hub/dashboard/', views.dashboard, name='dashboard'),
    path('hub/dashboard/ventas/', views.sales, name='ventas'),
    path('hub/dashboard/ventas/detalle/<int:sale_id>',views.sale_detail,name='ver_detalle_venta'),
    
    path('hub/dashboard/ovejas/', views.sheeps, name='ovejas'),
    # URLS para ver el detalle de la oveja con id_oveja = id
    path('hub/dashboard/oveja/detalle/<int:sheep_id>/', views.view_details, name='ver_detalle'),
    path('hub/dashboard/ovejas/detalle/eliminar/<int:sheep_id>/',views.delete_sheep,name='eliminar_oveja'),
    path('hub/dashboard/ovejas/detalle/editar/<int:sheep_id>/',views.edit_sheep,name="editar_ovino"),

    #descarga de tabla
    path('hub/dashboard/ovejas/descarga/',views.download_table,name='tabla_registro'),

    path('hub/dashboard/planteletas/', views.planteletas, name='planteletas'),

    # dashboard analisis de datos
    path('hub/dashboard/analisis/ventas/', views.sales_analysis, name='analisis_ventas'),
path('hub/dashboard/analisis/ovinos/', views.sheep_analysis, name='analisis_ovinos'),

    # API View
    path('api/ovejas/',views.SheepListAPI.as_view(),name='OvinoApi'),
    path('api/establecimiento/',views.EstablishmentAPI.as_view(),name='Establecimiento'),
    path('api/ventas/',views.SalesListAPI.as_view(),name='Venta'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
