from django.urls import path
from . import views

app_name = 'ganaderia'


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/ventas/', views.ventas, name='ventas'),
    path('dashboard/ovejas/', views.ovejas, name='ovejas'),
    path('dashboard/planteletas/', views.planteletas, name='planteletas'),
]
