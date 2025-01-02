from django.urls import path
from . import views

app_name = 'ganaderia'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/',views.logout_view,name='logout'),

    # URLS de dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/ventas/', views.ventas, name='ventas'),
    path('dashboard/ovejas/', views.ovejas, name='ovejas'),
    # URLS para ver el detalle de la oveja con id_oveja = id
    path('dashboard/oveja/detalle/<int:id_oveja>/', views.ver_detalle, name='ver_detalle'),
    path('dashboard/planteletas/', views.planteletas, name='planteletas'),
]
