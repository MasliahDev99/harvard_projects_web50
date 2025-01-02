from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from datetime import date
from .models import User
from .models import *


from .utils import crear_establecimiento,obtener_nombre_con_rut,obtener_todas_las_ovejas,obtener_todos_tipos_cantidad,agregar_oveja
from .utils import calcular_edad_por_fecha_nacimiento,obtener_padre_madre,existe_oveja,obtener_raza,obtener_calificador
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
    corderos, corderas, borregos, borregas, carneros, ovejas, total_ovejas = obtener_todos_tipos_cantidad(request)
    
    context = {
        'corderos': corderos,
        'corderas': corderas,
        'borregos': borregos,
        'borregas': borregas,
        'carneros': carneros,
        'ovejas': ovejas,
        'total_ovejas': total_ovejas,
    }
    
    return render(request, 'ganaderia/dashboard.html', context)

@login_required
def ventas(request):
    return render(request, 'ganaderia/ventas.html')



@login_required
def ovejas(request):
    ovejas = obtener_todas_las_ovejas(request)

    razas = Raza.objects.all()
    calificadores = CalificadorPureza.objects.all()
    
    if request.method == 'POST':
        nueva_oveja, mensaje = agregar_oveja(request)
        if nueva_oveja:
            messages.success(request, mensaje)
        else:
            messages.error(request, mensaje)
        return redirect('ganaderia:ovejas')

    for oveja in ovejas:
        oveja.edad_clasificada = oveja.clasificar_edad()

    return render(request, 'ganaderia/ovejas.html', {
        'ovejas': ovejas,
        'razas': razas,
        'calificadores': calificadores,
    })

@login_required
def ver_detalle(request, id_oveja):
    oveja = get_object_or_404(Oveja, id=id_oveja)
    return render(request, 'ganaderia/detalle.html',{
        'oveja': oveja,
    })



@login_required
def planteletas(request):
    return render(request, 'ganaderia/planteletas.html')