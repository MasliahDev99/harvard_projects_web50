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


def about(request):
    return render(request,'ganaderia/main.html')


def register_view(request):
    """

    Handles user registration, creates a new establishment if credentials are valid.

    """
    if request.method == 'POST':
        establishment = request.POST.get('username')
        RUT = request.POST.get('RUT')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirmation')
        breed_code = request.POST.get('criadorARU')

        if password != password2:
            return render(request,'ganaderia/register.html',{
                "message" : 'Password must match.',
            })
        try:   
            #cambio aqui
            new_establishment = utils.create_establishment(
                username=establishment,RUT=RUT,ARU_bred_code=breed_code,email=email,password=password
                )
            new_establishment.save()            

        except IntegrityError as e:
            return render(request,'ganaderia/register.html',{
                "message" : 'An establishment with these details already exists.',
            })
        login(request, new_establishment)
        return HttpResponseRedirect(reverse("ganaderia:index"))
    
    return render(request, 'ganaderia/register.html')

def login_view(request):
    """
    Handles user login and authenticates the establishment based on RUT and password.
    
    """
    if request.method == 'POST':
        RUT = request.POST.get('rut')
        password = request.POST.get('password')

        # cambio aqui 
        username = utils.get_name_by_rut(RUT)
        if username:
            establecimiento = authenticate(request,username=username, password = password)
            if establecimiento is not None:
                login(request,establecimiento)
                return redirect('ganaderia:dashboard')
            else:
                messages.error(request, 'Invalid credentials, Please try again.')
        else:
                messages.error(request, 'No establishment found with that RUT.')
    
    storage = get_messages(request)
    for _ in storage:
        pass

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
    #cambio aqui
    lambs_male, lambs_female, yearling_male, yearling_female, rams, ewes, total_sheeps = utils.get_sheep_count_by_type_and_age(request)
    sales = utils.sale_information(request) #return a dictionary 
    
    context = {
        'corderos': lambs_male,      # Male lambs (0-6 months)
        'corderas': lambs_female,    # Female lambs (0-6 months)
        'borregos': yearling_male,   # Young male sheep (6-12 months)
        'borregas': yearling_female, # Young female sheep (6-12 months)
        'carneros': rams,            # Adult male sheep (>12 months)
        'ovejas': ewes,              # Adult female sheep (>12 months)
        'total_sheeps': total_sheeps,
        'sales': sales,   
    }
    
    return render(request, 'ganaderia/dashboard.html', context)






@csrf_protect
@login_required
def sales(request):
    """
    Displays the list of sheep sold and allows creating new sales entries.
    """
    if request.method == 'POST':
        try:
            sale_type, by_lot, sheep_list, total_weight, price_per_kg, auction_total, sale_date, total_value, individual_prices = utils.get_frontend_data(request)

            if not all([sale_type, sheep_list, sale_date]):
                return JsonResponse({
                    'error': 'Missing required fields: sale_type, sheep list, and sale_date are required'
                }, status=400)

            try:
                selected_sheep = Oveja.objects.filter(id__in=sheep_list, establishment=request.user)
                
                if not selected_sheep.exists():
                    return JsonResponse({
                        'error': 'No valid sheep selected'
                    }, status=400)

                sale = utils.register_sale(
                    establishment=request.user,
                    sheeps=selected_sheep,
                    sale_type=sale_type,
                    sale_date=sale_date,
                    total_weight=total_weight,
                    price_per_kg=price_per_kg,
                    auction_total=auction_total,
                    total_value=total_value,
                    individual_prices=individual_prices
                )

                if sale is not None:
                    selected_sheep.update(status='sold')
                    return JsonResponse({
                        'success': True,
                        'message': 'Sale successfully registered'
                    })
                else:
                    return JsonResponse({
                        'error': 'Failed to register sale'
                    }, status=400)

            except IntegrityError as e:
                return JsonResponse({
                    'error': f'Database error: {str(e)}'
                }, status=400)
            except Exception as e:
                return JsonResponse({
                    'error': f'Unexpected error: {str(e)}'
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'error': f'Server error: {str(e)}'
            }, status=500)

    # GET request handling
    sales = Venta.objects.filter(establishment=request.user).annotate(
        sheep_count=Count('sheep'),
        calculated_total_weight=Coalesce(Sum('sheep__weight', output_field=FloatField()), 0.0)
    ).prefetch_related('sheep')
    
    #cambio aqui
    active_sheeps = utils.get_sheeps_by_status(request,'active')
    #active_sheeps = Oveja.objects.filter(establishment=request.user, status='active')

    for sale in sales:
        for sheep in sale.sheep.all():
            sheep.classified_age = sheep.classify_age()

    return render(request, 'ganaderia/ventas.html', {
        'sales': sales,
        'active_sheeps': active_sheeps,
    })



@login_required
def sheeps(request):
    """

    Displays all the sheep of the establishment, allows adding new ones and manages errors during the process.
    
    """ 
    #get active sheeps from the establishment
    sheep = utils.get_sheeps(request)

    breeds = Raza.objects.all()

    purity_qualifiers = CalificadorPureza.objects.all()  

    modal_open = False
    errors = []

    if request.method == 'POST':
        #cambio aqui
        new_sheep, messages_list = utils.add_sheep(request)
        #print the messages list to debug
        print(messages_list)
        if new_sheep:
            messages.success(request, messages_list[0])
            return redirect('ganaderia:ovejas')
        else:
            for message in messages_list:
                messages.error(request, message)
            errors = messages_list
            modal_open = True
    
    for sheep_item in sheep:
        sheep_item.edad_clasificada = sheep_item.classify_age()

    # Clear messages
    storage = get_messages(request)
    for _ in storage:
        pass

    return render(request, 'ganaderia/ovejas.html', {
        'sheeps': sheep,
        'razas': breeds,
        'purity_qualifiers': purity_qualifiers,
        'modal_open': modal_open,
        'errores': errors,
    })

@login_required
def view_details(request, sheep_id):
    """
        Display an specific sheep details of the establishment.
    """

    # get the sheep reference
    sheep = get_object_or_404(Oveja, id=sheep_id)
    sheep.edad_clasificada = sheep.classify_age()
    return render(request, 'ganaderia/detalle.html',{
        'sheep': sheep,
    })

@login_required
def delete_sheep(request,sheep_id):
    """
    Deletes an ovine record based on the provided ID.

    This function handles the deletion of an ovine either due to death or by mistake. 
    If the reason is death, it updates the status of the ovine to "dead" and records 
    the death reason along with the date of death. If the reason is an error, it deletes 
    the ovine completely.

    Args:
        request: The HTTP request object.
        sheep_id: The ID of the ovine to be deleted.

    Returns:
        HttpResponseRedirect: Redirects to the ovine details page or the ovines list page.
    """
     # Get the sheep object first
    sheep = get_object_or_404(Oveja, id=sheep_id)
    
    if request.method == 'POST':
        delete_reason = request.POST.get('delete_reason')
        observation = request.POST.get('death_reason')

        if delete_reason == 'muerte': 
           
           success,message = utils.update_status(
            sheep,
            'dead',
            observation = observation,
            death_date = date.today()
           )
           if not success:
               messages.error(request, message[0])
               return redirect('ganaderia:ver_detalle',sheep_id=sheep_id)
        elif delete_reason == 'error':
            sheep.delete()
        else:
            messages.error(request, 'Invalid deletion reason.')
            return redirect('ganaderia:ver_detalle', sheep_id=sheep_id)

        messages.success(request, f'The sheep RP: {sheep.RP if sheep.RP else sheep.id} has been successfully deleted.')
        return redirect('ganaderia:ovejas')
    return redirect('ganaderia:ver_detalle', sheep_id=sheep_id)


@login_required
def edit_sheep(request, sheep_id):
    """
    Edits an ovine's details, such as weight and RP number.

    This function allows the user to update the weight and RP number of an ovine. 
    If the RP number is changed, it validates the new RP and updates it accordingly. 
    If there are any validation errors, they are returned to the user for correction.

    Args:
        request: The HTTP request object.
        sheep_id: The ID of the ovine to be edited.

    Returns:
        HttpResponse: Redirects to the ovine detail page or displays error messages if validation fails.
    """
    sheep = get_object_or_404(Oveja, id=sheep_id, establishment=request.user)
    errors = []
    modal_open = False

    if request.method == 'POST':
        new_weight = request.POST.get('nuevo_peso')
        new_rp = request.POST.get('nuevo_rp')

        try:
            sheep.weight = float(new_weight)
        except (ValueError, TypeError):
            errors.append('The weight must be a valid number.')

        if not sheep.RP and new_rp:
            success, messages_list = utils.set_rp(new_rp=new_rp, sheep_id=sheep_id)
            if not success:
                errors.extend(messages_list)
                sheep.RP = None
            else:
                messages.success(request, messages_list[0])
                return redirect('ganaderia:ver_detalle', sheep_id=sheep_id)
        
        if errors:
            for message in errors:
                messages.error(request, message)
            modal_open = True
        else:
            sheep.save()
            messages.success(request, 'The sheep has  been succesfully updated.')
            return redirect('ganaderia:ver_detalle', sheep_id=sheep_id)

    context = {
        'sheep': sheep,
        'modal_open': modal_open,
        'errores': errors,
    }
    return render(request, 'ganaderia/detalle.html', context)

@csrf_protect
@login_required
def download_table(request):
    """
    Handles the download of ovine records in the format specified by the user.

    If the request is a POST, retrieves the desired file name and extension from the form, 
    generates the file, and returns it to the user for download.

    Returns:
        HttpResponse: The requested file in the specified format.
        HttpResponseRedirect: Redirects to the ovine page if the request is invalid.
    """
    if request.method == 'POST':
        filename = request.POST.get('nombre_archivo')
        extension = request.POST.get('extension')

      

        # Use the correct register_type
        response = utils_descargas.download_register(
            establishment=request.user,
            register_type='ovine_record',  
            filename=filename,
            extension=extension
        )
        messages.success(request, f'The file {filename} has been successfully downloaded on Downloads directory.')

    return redirect('ganaderia:ovejas')




@login_required
def sale_detail(request, sale_id):
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
    sale = get_object_or_404(Venta, id=sale_id)
    
    # Calculate total and average weight
    total_weight = sale.sheep.aggregate(total=Sum('weight'))['total'] or 0
    average_weight = total_weight / sale.sheep.count() if sale.sheep.count() > 0 else 0
 
    context = {
        'sale': sale,
        'total_weight': total_weight,
        'average_weight': average_weight,
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
    ovejas = utils.get_sheeps(request)
    
    for oveja in ovejas:
        oveja.edad_clasificada = oveja.classify_age()
    


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
def sales_analysis(request):
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
def sheep_analysis(request):
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
class SheepListAPI(APIView):
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
        active_sheep = Oveja.objects.filter(establishment=request.user, status='active')
        serializer = OvejaSerializer(active_sheep, many=True)
        return Response(serializer.data)


# API VIEW PARA VENTAS DEL ESTABLECIMIENTO
class SalesListAPI(APIView):
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
        sales = Venta.objects.filter(establishment=request.user)
        serializer = VentaSerializer(sales, many=True)
        return Response(serializer.data)
    

# API VIEW PARA EL ESTABLECIMIENTO 
class EstablishmentAPI(APIView):
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
    def get(self, request):
        establishment = User.objects.filter(RUT=request.user.RUT).first()
        serializer = EstablecimientoSerializer(establishment, many=False, context={'request': request})
        return Response(serializer.data)
    

