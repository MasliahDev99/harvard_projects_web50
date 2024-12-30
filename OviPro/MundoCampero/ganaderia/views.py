from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import User
from .models import *


from .utils import crear_establecimiento,obtener_nombre_con_rut,obtener_todas_las_ovejas,obtener_todos_tipos_cantidad
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
    if request.method == 'POST':
        RUT = request.POST.get('rut')
        password = request.POST.get('password')

        #obtenemos el nombre del establecimiento
        username = obtener_nombre_con_rut(RUT)
        if username:
            establecimiento = authenticate(request,username=username, password = password)
            if establecimiento is not None:
                login(request,establecimiento)
                return redirect('ganaderia:dashboard')
            
    return render(request, 'ganaderia/login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request,'ganaderia/index.html')

@login_required
def dashboard(request):
    ovejas = obtener_todas_las_ovejas()
    #ventas = obtener_todas_las_ventas()
    corderos,corderas,borregos,borregas,_,_,total_ovejas = obtener_todos_tipos_cantidad()
    return render(request, 'ganaderia/dashboard.html',{
        'ovejas' : ovejas,
        'corderos':corderos,
        'corderas': corderas,
        'borregos': borregos,
        'borregas' : borregas,
        'total_ovejas': total_ovejas,
    })

@login_required
def ventas(request):
    return render(request, 'ganaderia/ventas.html')

@login_required
def ovejas(request):
    ovejas = Oveja.objects.all()
    
    # Clasificar las edades de las ovejas antes de pasarlas al template
    for oveja in ovejas:
        oveja.edad_clasificada = oveja.clasificar_edad()  # Asignamos la clasificación de edad a una nueva propiedad

    return render(request, 'ganaderia/ovejas.html', {'ovejas': ovejas})

@login_required
def planteletas(request):
    return render(request, 'ganaderia/planteletas.html')