from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'ganaderia/index.html')





def register_view(request):
    return render(request, 'ganaderia/register.html')

def login_view(request):
    return render(request, 'ganaderia/login.html')


#@login_required
def dashboard(request):
    return render(request, 'ganaderia/dashboard.html')

def ventas(request):
    return render(request, 'ganaderia/ventas.html')

def ovejas(request):
    return render(request, 'ganaderia/ovejas.html')

def planteletas(request):
    return render(request, 'ganaderia/planteletas.html')