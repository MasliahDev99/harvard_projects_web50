from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import date
from .models import User
from .models import *
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import OvejaSerializer,VentaSerializer,EstablecimientoSerializer
from django.views.decorators.csrf import csrf_protect

from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Coalesce

import json

from . import utils
from . import utils_descargas
# Create your views here.

def index(request):
    """
        render the homepage view.
    """
    
    return render(request, 'ganaderia/index.html')





def register_view(request):
    """

    Handles user registration, creates a new establishment if credentials are valid.

    """
    if request.method == 'POST':
        establecimiento = request.POST.get('username')
        RUT = request.POST.get('RUT')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirmation')
        codigo_criador = request.POST.get('criadorARU')

        if password != password2:
            return render(request,'ganaderia/register.html',{
                "message" : 'Las contraseña deben coincidir',
            })
        
        # corroboramos que el codigo criador de ARU no este registrado en la app
        
        #procedemos a crear el usuario establecimiento
        try:
            nuevo_establecimiento = utils.crear_establecimiento(
                username=establecimiento,RUT=RUT,codigo_criador_ARU=codigo_criador,email=email,password=password)
            nuevo_establecimiento.save()            

        except IntegrityError as e:
            return render(request,'ganaderia/register.html',{
                "message" : 'Ya existe un establecimiento con esos datos',
            })
        login(request, nuevo_establecimiento)
        return HttpResponseRedirect(reverse("ganaderia:index"))
        
    return render(request, 'ganaderia/register.html')

def login_view(request):
    """
    Handles user login and authenticates the establishment based on RUT and password.
    
    """
    if request.method == 'POST':
        RUT = request.POST.get('rut')
        password = request.POST.get('password')

        #obtenemos el nombre del establecimiento
        username = utils.obtener_nombre_con_rut(RUT)
        if username:
            establecimiento = authenticate(request,username=username, password = password)
            if establecimiento is not None:
                login(request,establecimiento)
                return redirect('ganaderia:dashboard')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, intente nuevamente.')
        else:
                messages.error(request, 'No se encontró un establecimiento con ese RUT.')
    
    return render(request, 'ganaderia/login.html')

@login_required
def logout_view(request):
    """
    Logs the user out and redirects to the homepage.

    """
    logout(request)
    return render(request,'ganaderia/index.html')

@login_required
def dashboard(request):
    """
    Displays a summary of the establishment's sheep and sales data.

    """
    #obtenemos el resumen de los ovinos que tiene el establecimiento
    corderos, corderas, borregos, borregas, carneros, ovejas, total_ovejas = utils.obtener_todos_tipos_cantidad(request)
    #obtenemos el resumen de las ventas del establecimiento 
    ventas = utils.informacion_de_ventas(request) #diccionario
    
    context = {
        'corderos': corderos,
        'corderas': corderas,
        'borregos': borregos,
        'borregas': borregas,
        'carneros': carneros,
        'ovejas': ovejas,
        'total_ovejas': total_ovejas,
        'ventas': ventas,   
    }
    
    return render(request, 'ganaderia/dashboard.html', context)



def obtener_datos_front(request):
    """
    Processes and extracts data from the frontend JSON request.
    Returns the extracted parameters.
    """
    # Intentamos leer los datos del request.body si está en formato JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}

    # Extraemos parámetros del JSON
    tipo_venta = data.get('tipo_venta', None)
    por_lote = data.get('por_lote', False)
    ovinos = data.get('ovinos', [])
    peso_total = data.get('peso_total', None)
    precio_kg = data.get('precio_kg', None)
    remate_total = data.get('remate_total', None)
    fecha_venta = data.get('fecha_venta', None)
    valor_total = data.get('valor_total', None)

    return tipo_venta, por_lote, ovinos, peso_total, precio_kg, remate_total, fecha_venta, valor_total


@csrf_protect
@login_required
def ventas(request):
    """
    Displays the list of sheep sold and allows creating new sales entries.
    
    """
    #obtenemos las ventas del establecimiento
    ventas = Venta.objects.filter(establecimiento=request.user).annotate(
        oveja_count=Count('ovejas'),
        peso_total_calculado=Coalesce(Sum('ovejas__peso', output_field=FloatField()), 0.0)
    ).prefetch_related('ovejas')
    #obtenemos todos los ovinos que tiene el establecimiento registrado
    lista_ovejas = Oveja.objects.filter(establecimiento=request.user,estado='activa')


    for venta in ventas:
        for oveja in venta.ovejas.all():
            oveja.edad_clasificada = oveja.clasificar_edad()

    
    if request.method == 'POST':
        print("capturamos los datos enviados del frontend")
        try:
            tipo_venta, por_lote, ovinos, peso_total, precio_kg, remate_total, fecha_venta, valor_total = obtener_datos_front(request)
            try:
                ovejas = Oveja.objects.filter(RP__in=ovinos,establecimiento = request.user)

                venta = utils.registrar_venta(
                                        establecimiento=request.user,
                                        lista_ovejas= ovejas,
                                        tipo_venta=tipo_venta,
                                        fecha_venta=fecha_venta,
                                        peso_total= peso_total,
                                        precio_kg=precio_kg,
                                        remate_total=remate_total,
                                        valor_total=valor_total,
                                        
                    )
                if venta is not None:
                    print("El objeto venta se ha gestionado.\n")
                else:
                    print("La venta fue None")
            except IntegrityError:
                print("\nEntro al try y hubo un error en 'registrar_venta'\n")
                return JsonResponse({'Error': 'Error al registrar la venta'},status = 400)
            
            
            #asociamos las ovejas vendidas del establecimiento
            venta.ovejas.set(ovejas)
            #marcamos los ovinos de la tabla de registro como vendidos
            ovejas.update(estado='vendida')


            return JsonResponse({'success': 'Venta registrada exitosamente'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


    return render(request, 'ganaderia/ventas.html',{
        'ventas': ventas,
        'lista_ovejas': lista_ovejas,

    })





@login_required
def ovejas(request):
    """

    Displays all the sheep of the establishment, allows adding new ones and manages errors during the process.
    
    """

    storage = get_messages(request)
    for _ in storage:  # Iterar por el almacenamiento para limpiarlo
        pass
    ovejas = utils.obtener_todas_las_ovejas(request)
    razas = Raza.objects.all()
    calificadores = CalificadorPureza.objects.all()  

    modal_abierto = False
    errores = []

    if request.method == 'POST':
        nueva_oveja, mensajes = utils.agregar_oveja(request)
        print(mensajes)
        if nueva_oveja:
            messages.success(request, mensajes[0])
            return redirect('ganaderia:ovejas')
        else:
            for mensaje in mensajes:
                messages.error(request, mensaje)
            errores = mensajes
            modal_abierto = True
    
    for oveja in ovejas:
        oveja.edad_clasificada = oveja.clasificar_edad()

    return render(request, 'ganaderia/ovejas.html', {
        'ovejas': ovejas,
        'razas': razas,
        'calificadores': calificadores,
        'modal_abierto': modal_abierto,
        'errores':errores,
    })

@login_required
def ver_detalle(request, id_oveja):
    """
        Display an specific sheep details of the establishment.
    """
    oveja = get_object_or_404(Oveja, id=id_oveja)
    oveja.edad_clasificada = oveja.clasificar_edad()

    return render(request, 'ganaderia/detalle.html',{
        'oveja': oveja,
    })

@login_required
def eliminar_oveja(request,id_oveja):
    """
    Deletes an ovine record based on the provided ID.

    This function handles the deletion of an ovine either due to death or by mistake. 
    If the reason is death, it updates the status of the ovine to "dead" and records 
    the death reason along with the date of death. If the reason is an error, it deletes 
    the ovine completely.

    Args:
        request: The HTTP request object.
        id_oveja: The ID of the ovine to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the ovine details page or the ovines list page.
    """
    oveja = get_object_or_404(Oveja,id=id_oveja)
    if request.method == 'POST':
        motivo_eliminacion = request.POST.get('delete_reason')
        observacion = request.POST.get('death_reason')

        if motivo_eliminacion == 'muerte': 
            # si el motivo es por fallecimiento entonces, guardamos en observacion del ovino su motivo y cambiamos el estado
            oveja.estado = 'muerta'
            oveja.observaciones = observacion
            # fecha de muerte 
            oveja.fecha_muerte = date.today()
            oveja.save()
            
        elif motivo_eliminacion == 'error':
            # si el motivo fue por error entonces se elimina la oveja
            oveja.delete()
        else:
            messages.error(request, 'Motivo de eliminación no válido.')
            return redirect('ganaderia:ver_detalle', id_oveja=id_oveja)

        messages.success(request,f'El ovino RP: {oveja.RP} ha sido eliminado con exito')
        return redirect('ganaderia:ovejas')
    return redirect('ganaderia:ver_detalle',id_oveja=id_oveja)


@login_required
def editar_oveja(request, id_oveja):
    """
    Edits an ovine's details, such as weight and RP number.

    This function allows the user to update the weight and RP number of an ovine. 
    If the RP number is changed, it validates the new RP and updates it accordingly. 
    If there are any validation errors, they are returned to the user for correction.

    Args:
        request: The HTTP request object.
        id_oveja: The ID of the ovine to be edited.

    Returns:
        HttpResponse: Redirects to the ovine detail page or displays error messages if validation fails.
    """
    oveja = get_object_or_404(Oveja, id=id_oveja, establecimiento=request.user)
    errores = []
    modal_abierto = False

    if request.method == 'POST':
        nuevo_peso = request.POST.get('nuevo_peso')
        nuevo_rp = request.POST.get('nuevo_rp')

        try:
            oveja.peso = float(nuevo_peso)
        except (ValueError, TypeError):
            errores.append('El peso debe ser un número válido.')

        if not oveja.RP and nuevo_rp:
            # exitoso -> Bool, mensaje -> list[str]
            exitoso, mensajes = utils.set_rp(nuevo_RP=nuevo_rp, id_oveja=id_oveja)
            #si no fue exitoso, agregamos a la lista de errores los mensajes y reiniciamos el RP
            if not exitoso:
                errores.extend(mensajes)
                oveja.RP = None  # Resetea el RP si es invalido
            else:
                #si fue exitoso 
                messages.success(request,mensajes[0])
                return redirect('ganaderia:ver_detalle',id_oveja=id_oveja)
        
        if errores:
            for mensaje in errores:
                messages.error(request, mensaje)
            modal_abierto = True
        else:
            oveja.save()
            messages.success(request, 'El ovino ha sido actualizado exitosamente.')
            return redirect('ganaderia:ver_detalle', id_oveja=id_oveja)

    context = {
        'oveja': oveja,
        'modal_abierto': modal_abierto,
        'errores': errores,
    }
    return render(request, 'ganaderia/detalle.html', context)


@login_required
def descargar_tabla(request):
    """
    Handles the download of ovine records in the format specified by the user.

    If the request is a POST, retrieves the desired file name and extension from the form, 
    generates the file, and returns it to the user for download.

    Returns:
        HttpResponse: The requested file in the specified format.
        HttpResponseRedirect: Redirects to the ovine page if the request is invalid.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre_archivo')
        ext = request.POST.get('extension')

        respuesta = utils_descargas.descargar_registro(request.user,'registro_ovino',nombre_archivo=nombre,extension=ext)
        messages.success(request,f'Se ha descargado con exito el archivo {nombre}')

    return redirect('ganaderia:ovejas')




@login_required
def detalle_venta(request, id_venta):
    """
    Displays detailed information about a specific sale.

    This function calculates the total and average weight of the sheep involved in a sale 
    and provides this information to the user.

    Args:
        request: The HTTP request object.
        id_venta: The ID of the sale to view.

    Returns:
        HttpResponse: The sale details along with the total and average weight of the sheep.
    """
    venta = get_object_or_404(Venta, id=id_venta)
    
    # Calcular el peso total y promedio
    peso_total = venta.ovejas.aggregate(total=Sum('peso'))['total'] or 0
    peso_promedio = peso_total / venta.ovejas.count() if venta.ovejas.count() > 0 else 0

    context = {
        'venta': venta,
        'peso_total': peso_total,
        'peso_promedio': peso_promedio,
    }
    
    return render(request, 'ganaderia/detalleVenta.html', context)



@login_required
def planteletas(request):
    """
    Displays the list of all sheep available for planting.

    This view retrieves all the sheep records for the current establishment and displays them 
    on a planting page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the planting page with the list of sheep.
    """
    ovejas = utils.obtener_todas_las_ovejas(request)
    for oveja in ovejas:
        oveja.edad_clasificada = oveja.clasificar_edad()


    # traemos los ovinos que esten en los planteles

    return render(request, 'ganaderia/planteletas.html',{
        'ovejas': ovejas,
    })


@login_required
def hub(request):
    """
    Displays the main hub of the ovine management platform.

    This is the central page where users can access different sections of the platform.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the ovine hub page.
    """
    return render(request, 'ganaderia/OvinoHub.html')


@login_required
def analisis_ventas(request):
    """
    Displays the sales analysis dashboard.

    This view presents a dashboard where users can analyze their sales data.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the sales analysis page.
    """
    return render(request, 'ganaderia/components/dashboard/DatosVentas.html')


@login_required
def analisis_ovinos(request):
    """
    Displays the ovine analysis dashboard.

    This view presents a dashboard where users can analyze data about their sheep.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the ovine analysis page.
    """
    return render(request, 'ganaderia/components/dashboard/DatosOvinos.html')


# API VIEW  PARA LOS OVINOS DEL ESTABLECIMIENTO
class OvejaListadoAPI(APIView):
    """
    API view for listing the sheep records for the user's establishment.

    This API returns all active sheep belonging to the user's establishment.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The serialized list of active sheep for the user's establishment.
    """
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        # Filtramos las ovejas asociadas al establecimiento del usuario actual
        ovejas = Oveja.objects.filter(establecimiento=request.user,estado='activa')
        serializer = OvejaSerializer(ovejas, many=True)  # Usamos el serializer correcto
        return Response(serializer.data)


# API VIEW PARA VENTAS DEL ESTABLECIMIENTO
class VentaListadoAPI(APIView):
    """
    API view for listing the sales records for the user's establishment.

    This API returns all sales records associated with the user's establishment.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The serialized list of sales for the user's establishment.
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Filtrar las ventas del establecimiento del usuario actual
        ventas = Venta.objects.filter(establecimiento=request.user)
        # Usamos el serializador y pasamos el contexto con el request para poder acceder al establecimiento
        serializer = VentaSerializer(ventas, many=True)  
        # Devolvemos la respuesta con los datos serializados
        return Response(serializer.data)
    

# API VIEW PARA EL ESTABLECIMIENTO 
class EstablecimientoAPI(APIView):
    """
    API view for retrieving the user's establishment details.

    This API returns the details of the user's establishment, including information 
    like the establishment name and user information.

    Args:
        request: The HTTP request object.

    Returns:
        Response: The serialized establishment details.
    """
    permission_classes = [IsAuthenticated]
    def get(self,request):
        establecimiento = User.objects.filter(RUT=request.user.RUT).first()
        serializer = EstablecimientoSerializer(establecimiento,many=False,context={'request': request})
        return Response(serializer.data)
    

