from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import User
from .models import *

from .utils import crear_establecimiento
# Create your views here.

def index(request):
    return render(request, 'ganaderia/index.html')





def register_view(request):
    if request.method == 'POST':
        establecimiento = request.POST.get('username')
        RUT = request.POST.get('RUT')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirmation')

        if password != password2:
            return render(request,'ganaderia/register.html',{
                "message" : 'Las contraseña deben coincidir',
            })
        
        #procedemos a crear el usuario establecimiento
        try:
            nuevo_establecimiento = crear_establecimiento(
                username=establecimiento,RUT=RUT,email=email,password=password)
            nuevo_establecimiento.save()            

        except IntegrityError as e:
            return render(request,'ganaderia/register.html',{
                "message" : 'Ya existe un establecimiento con esos datos',
            })
        login(request, nuevo_establecimiento)
        return HttpResponseRedirect(reverse("ganaderia:index"))
        
    return render(request, 'ganaderia/register.html')

def login_view(request):
    return render(request, 'ganaderia/login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request,'ganaderia/index.html')

@login_required
def dashboard(request):
    return render(request, 'ganaderia/dashboard.html')

@login_required
def ventas(request):
    return render(request, 'ganaderia/ventas.html')

@login_required
def ovejas(request):
    return render(request, 'ganaderia/ovejas.html')

@login_required
def planteletas(request):
    return render(request, 'ganaderia/planteletas.html')