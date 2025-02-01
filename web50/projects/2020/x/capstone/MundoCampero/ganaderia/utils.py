import json
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Raza,CalificadorPureza,Oveja,Venta
from datetime import date,datetime
from django.db.models import Sum


from django.template.loader import get_template


"""
    Purpose:
    This file serves as a central repository for utility functions used throughout 
    the project. These utility functions provide reusable logic for various operations, 
    such as database queries, validations, and data processing, ensuring a clean and maintainable 
    codebase by reducing redundancy in views or other modules.


"""




def create_establishment(username,RUT,ARU_bred_code,email,password):
    """
    Creates a new establishment (user) in the database.

    Args:
        username (str): The name of the establishment.
        RUT (int): Unique number(12) Identification Code for the establishment.
        codigo_criador_ARU (int): ARU (Rural Association) breeder code.
        email (str): Email address for the establishment.
        password (str): Password for the user account.

    Returns:
        User: The newly created user instance.

    Raises:
        IntegrityError: If an establishment with the given RUT already exists.
    """
    if exists_establishment(RUT):
        raise IntegrityError("The RUT is already exists.")
    
    nuevo_establecimiento = User(username=username,RUT=RUT,email=email,password=password,ARU_bred_registration = ARU_bred_code)
    nuevo_establecimiento.set_password(password) # ciframos la contrasenia
    nuevo_establecimiento.save()

    return nuevo_establecimiento

def exists_establishment(RUT=None):

    """
        Checks if an establishment exists in the database based on Its Rut.

        Args:
            RUT (int): Identification Code to check.
           
        Returns:
            bool: True if the establishment exists, False otherwise.
    """
    
    return User.objects.filter(RUT=RUT).exists()

def get_name_by_rut(RUT):
    """
    Retrieves the name of an establishment by its RUT.

    Args:
        RUT (int): Identification Code of the establishment.

    Returns:
        str: The name of the establishment if found, otherwise None.
    """
    if exists_establishment(RUT):
        establishment = User.objects.get(RUT=RUT)
        return establishment.username
    return None



# sheep_managment

def get_race(raza_nombre):
    """
    Retrieves a breed instance by its name.

    Args:
        raza_nombre (str): Name of the breed.

    Returns:
        Raza: The corresponding breed instance.

    Raises:
        ObjectDoesNotExist: If the breed is not found.
    """
    return Raza.objects.get(name=raza_nombre)

def get_purity_qualifier(purity):
    """
    Retrieves a purity qualifier by its name.

    Args:
        purity (str): Name of the qualifier.

    Returns:
        CalificadorPureza: The corresponding purity qualifier instance.

    Raises:
        ObjectDoesNotExist: If the qualifier is not found.
    """
    return CalificadorPureza.objects.get(name = purity)

def get_sheeps(request):
    """
    Retrieves all active sheep associated with the logged-in user's establishment.

    Args:
        request (HttpRequest): The current HTTP request containing user information.

    Returns:
        QuerySet: A list of active sheep for the user's establishment.
    """
    return Oveja.objects.filter(establishment = request.user,status='active')

def get_sheeps_by_status(request,status='active'):
    """
    retrieves all sheeps by an specific status (active,dead,sold,stolen)

    Args:
        request (HttpRequest): The current HTTP request containing user information.
        status (str, optional): The status of the sheeps. Defaults to 'active'.
    Returns:
        QuerySet: A list of sheeps for the user's establishment.

    """
    return Oveja.objects.filter(establishment = request.user,status=status)

def get_sheep_count_by_type_and_age(request):
    """
    Retrieves the count of all sheep categorized by type and age group.

    Args:
        request (HttpRequest): The current HTTP request containing user information.

    Returns:
        tuple: Counts for corderos, corderas, borregos, borregas, carneros, ovejas, and total sheep.
    """
    user_ovejas = Oveja.objects.filter(establishment=request.user,status='active')
    
    corderos = user_ovejas.filter(age__lte=6, sex='Male').count()
    corderas = user_ovejas.filter(age__lte=6, sex='Female').count()
    borregos = user_ovejas.filter(age__gt=6, age__lte=12, sex='Male').count()
    borregas = user_ovejas.filter(age__gt=6, age__lte=12, sex='Female').count()
    
    carneros = user_ovejas.filter(age__gt=12, sex='Male').count()
    ovejas = user_ovejas.filter(age__gt=12, sex='Female').count()
    
    all_sheeps = user_ovejas.count()

    return corderos, corderas, borregos, borregas, carneros, ovejas, all_sheeps


def get_sheep(rp=None, id=None):
    """
    Retrieves a sheep by its RP or ID.

    Args:
        rp (int, optional): The RP (Permanent Record) of the sheep.
        id (int, optional): The unique ID of the sheep.

    Returns:
        Oveja: The corresponding sheep instance if found, otherwise None.
    """
    try:
        if rp:
            return Oveja.objects.get(RP=rp)
        if id:
            return Oveja.objects.get(id=id)
        else:
            return None
    except ObjectDoesNotExist:
        return None  # O puedes devolver un mensaje personalizado



   
def exists_sheep(RP=None, id=None):
    """
    Checks if a sheep exists in the database based on its RP or BU.

    Args:
        RP (int, optional): The RP of the sheep.
        id (int, optional): The primary key  of the sheep.

    Returns:
        bool: True if a sheep with the given RP or BU exists, False otherwise.
    """
    if RP and Oveja.objects.filter(RP=RP).exists():
        return True
    if id and Oveja.objects.filter(id=id).exists():
        return True
    return False



def calculate_age_by_birthdate(fecha_nacimiento):
    """
    Calculates the age in months from the birth date.

    Args:
        fecha_nacimiento (date): Birth date of the sheep.

    Returns:
        int: Age in months.
    """
    fecha_actual = date.today()  # Objeto date
    anios_dif = fecha_actual.year - fecha_nacimiento.year
    meses_dif = fecha_actual.month - fecha_nacimiento.month

    
    if meses_dif < 0:
        anios_dif -= 1
        meses_dif += 12

    edad_en_meses = anios_dif * 12 + meses_dif

    return edad_en_meses

def get_parents(rp_father, rp_mother):
    """
    Retrieves instances of the father and mother sheep if they exist.

    Args:
        rp_padre (int): RP of the father.
        rp_madre (int): RP of the mother.

    Returns:
        tuple: Instances of the father and mother sheep, or None if not found.
    """
    father = Oveja.objects.filter(RP=rp_father).first() if rp_father else None
    mother = Oveja.objects.filter(RP=rp_mother).first() if rp_mother else None
    return father,mother


def validate_parents(sheep_father, sheep_mother, RP):
    """
    Validates that the father and mother are not the same and that the sheep is not its own parent.

    Args:
        sheep_father (int): RP of the father.
        sheep_mother (int): RP of the mother.
        RP (int): RP of the sheep being registered.
        
    Returns:
        list: A list of validation errors, or an empty list if valid.
    """
    errores = []

    if sheep_father== sheep_mother:
        errores.append("El padre y la madre no pueden ser el mismo animal.")
    if RP in [sheep_father, sheep_mother]:
        errores.append("El ovino no puede ser su propio padre o madre.")

    return errores

def exists_sheep_name(name,establishment):
    """
    Checks if a sheep with the given name exists for the specified establishment.
    Args:
        name (str): The name of the sheep.
        establishment (User): The establishment associated with the sheep.
    Returns:
        bool: True if a sheep with the given name exists, False otherwise.
    """
    return Oveja.objects.filter(name__iexact=name,establishment=establishment).exists()

def generate_unique_name():
    """
    Generates a unique name using a UUID.

    Returns:
        str: A unique name.
    """
    import uuid
    return f"SinNombre-{uuid.uuid4().hex[:8]}" 





def validate_birthdate(birth_date):
    """
    Validates that a given birth date is not in the future.

    Args:
        birth_date (date): Birth date to validate.

    Returns:
        str or None: An error message if invalid, or None if valid.
    """
    if birth_date > date.today():
        return "La fecha de nacimiento no puede ser futura."
    return None

def get_sheep_form_data(request):
    """
    Captures data sent from the ovine registration form and returns it.
    If some fields are not present, defaults to `None` or `False`.

    Args:
        request (HttpRequest): The HTTP request containing form data.

    Returns:
        tuple: A tuple containing the captured values from the form:
            - BU (int or None): The internal identifier for the ovine.
            - RP (int or None): The permanent record identifier for the ovine.
            - nombre (int or None): The name of the ovine.
            - peso (int or None): The weight of the ovine in kilograms.
            - raza (int or None): The breed of the ovine.
            - fecha_nacimiento (str or None): The birth date of the ovine.
            - sexo (str or None): The gender of the ovine ('Macho' or 'Hembra').
            - calificador_pureza (str or None): The purity qualifier of the ovine.
            - observacion_seleccionada (bool): Whether observations were marked in the form.
            - oveja_comprada (bool): Whether the ovine was marked as purchased.
    """
    BU = request.POST.get('BU', None)  # Puede ser None si no se especifica
    RP = request.POST.get('RP', None)  # Si no se proporciona, será None
    nombre = request.POST.get('nombre_animal', None)  # Igual para el nombre
    peso = request.POST.get('peso', None)  # Puede ser None si no se ingresa
    raza = request.POST.get('raza', None)
    fecha_nacimiento = request.POST.get('fecha_nacimiento', None)
    sexo = request.POST.get('sexo', None)
    calificador_pureza = request.POST.get('calificador_pureza', None)
    observacion_seleccionada = request.POST.get('obs') == 'on'  # Captura como booleano
    oveja_comprada = request.POST.get('purchased') == 'on'  # Captura como booleano

    return BU, RP, nombre, peso, raza, fecha_nacimiento, sexo, calificador_pureza, observacion_seleccionada, oveja_comprada




def add_sheep(request):
    """
    Método para agregar ovejas.

    Args:
        request (HttpRequest): Objeto de solicitud HTTP que contiene los datos enviados desde el formulario.

    Returns:
        tuple:
            - Oveja (Oveja): Instancia de la oveja creada (si no hay errores).
            - list: Lista de mensajes de error.

    Raises:
        IntegrityError: Si ocurre un problema al guardar los datos en la base de datos.

    Ejemplo:
        request = {
            'POST': {
                'BU': '123',
                'RP': '456',
                'nombre': 'Oveja1',
                ...
            },
            'user': <User object>
        }
        oveja, errores = agregar_oveja(request)
    """
    errors = []

    # Get form data
    BU, RP, name, weight, breed, birth_date, sex, purity_qualifier, has_observations, is_purchased = get_sheep_form_data(request)
    observations = None
    establishment = request.user

    # Check if sheep exists by RP
    if RP and exists_sheep(RP=RP):
        errors.append(f"A sheep with RP {RP} already exists.")

    father_sheep, mother_sheep = None, None

    # Pedigree validation
    if purity_qualifier == 'pedigri':
        father_sheep = request.POST.get('oveja_padre')
        mother_sheep = request.POST.get('oveja_madre')
        
        if not RP:
            errors.append("The RP field is required for pedigree purity.")
        if mother_sheep and father_sheep:
            validation_errors = validate_parents(father_sheep, mother_sheep, RP)
            if validation_errors:
                errors.extend(validation_errors)
    else:
        RP = None

    # Validate purchased sheep
    origin = None
    if is_purchased:
        origin = request.POST.get('origen')
        if not origin:
            origin = 'Not specified.'

    # Validate birth date
    try:
        birth_date = date.fromisoformat(birth_date)
        if birth_date > date.today():
            errors.append("The birth date cannot be greater than current date.")
    except ValueError:
        errors.append("Invalid date format. Use the format YYYY-MM-DD.")

    # Calculate age if no errors
    if not errors:
        age = calculate_age_by_birthdate(birth_date)

    # Get observations
    observations = request.POST.get('observaciones') if has_observations else None

    # Get breed and purity qualifier
    try:
        breed = get_race(breed)
        purity_qualifier = get_purity_qualifier(purity_qualifier)
    except ObjectDoesNotExist:
        errors.append("Raza o calificador de pureza no encontrado.")

    # Handle name
    if not name:
        name = generate_unique_name()
    else:
        if exists_sheep_name(name=name, establishment=establishment):
            errors.append(f"A sheep with the name {name} is registered in this establishment.")

    if errors:
        return None, errors

    try:
        new_sheep = Oveja.objects.create(
            BU=BU,
            RP=RP,
            name=name,
            weight=weight,
            raza=breed,
            age=age,
            birth_date=birth_date,
            sex=sex,
            purity_qualifier=purity_qualifier,
            notes=observations,
            father=father_sheep,
            mother=mother_sheep,
            establishment=establishment,
            origin_establishment=origin,
        )
        return new_sheep, ["Sheep registered succesfully"]
    except IntegrityError as e:
        return None, [f"Error registering the sheep: {str(e)}"]


def set_rp(new_rp: str, sheep_id: int):
    """
    Updates the RP of a sheep with a new identifier.

    Args:
        new_rp (str): The new RP to assign.
        sheep_id (int): The ID of the sheep to update.

    Returns:
        tuple: A boolean indicating success and a list with a message:
            - (True, [message]) if the RP is successfully updated.
            - (False, [error message]) if the RP already exists or the sheep does not exist.
    """
    try:
        oveja = Oveja.objects.get(id=sheep_id)
    except Oveja.DoesNotExist:
        return False, [f"No sheep found with ID {sheep_id}."]
    
    if Oveja.objects.filter(RP=new_rp).exists():
        return False, [f"Error: A sheep with RP: {new_rp} already exists ."]
    
    oveja.RP = new_rp
    oveja.save()
    return True, [f"RP succesfully update to {new_rp} for sheep with ID {sheep_id}."]

def update_status(sheep, new_status: str, observation: str = None, death_date=None):
    """
    Updates the status of a sheep and performs related actions based on the new status.

    Args:
        sheep (Oveja): The sheep object to update.
        new_status (str): The new status to set for the sheep ('dead', 'sold', 'stolen').
        observation (str, optional): Additional notes or observations. Defaults to None.
        death_date (date, optional): The date of death, if applicable. Defaults to None.

    Returns:
        tuple: A boolean indicating success and a list with a message:
            - (True, [message]) if the status is successfully updated.
            - (False, [error message]) if the status is invalid.
    """
    status_actions = {
        'dead': lambda: update_dead_status(sheep, observation, death_date),
        'sold': lambda: update_sold_status(sheep),
        'stolen': lambda: update_stolen_status(sheep)
    }

    if new_status not in status_actions:
        return False, [f"Error: Invalid status {new_status}."]

    status_actions[new_status]()
    sheep.status = new_status
    sheep.save()
    return True, [f"Status successfully updated to {new_status} for sheep with ID {sheep.id}."]

def update_dead_status(sheep, observation, death_date):
    """
    Updates the sheep's status to 'dead' and sets the observation and death date.

    Args:
        sheep (Oveja): The sheep object to update.
        observation (str, optional): Additional notes or observations. Defaults to 'No observation provided.'
        death_date (date, optional): The date of death. Defaults to today's date.
    """
    sheep.notes = observation if observation else 'No observation provided.'
    sheep.death_date = death_date if death_date else date.today()

def update_sold_status(sheep):
    """
    Updates the sheep's status to 'sold' and sets the observation to indicate the sheep was sold.

    Args:
        sheep (Oveja): The sheep object to update.
    """
    sheep.notes = 'Sheep sold.'

def update_stolen_status(sheep):
    sheep.notes = 'Sheep stolen.'



# sales managment
    
    
def get_frontend_data(request):
    """
    Processes and extracts data from the frontend JSON request.
    Returns the extracted parameters.
    """
    # try read the JSON data
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = {}

    sale_type = data.get('tipo_venta', None)
    by_lot = data.get('por_lote', False)
    sheep_list = data.get('ovinos', [])
    total_weight = data.get('peso_total', None)
    price_per_kg = data.get('precio_kg', None)
    auction_total = data.get('remate_total', None)
    sale_date = data.get('fecha_venta', None)
    total_value = data.get('valor_total', None)
    individual_price = data.get('precio_individual', None)

    return sale_type, by_lot, sheep_list, total_weight, price_per_kg, auction_total, sale_date, total_value, individual_price


# ventas, metodo de ventas

def register_sale(establishment, sheeps, sale_type, sale_date, total_weight=None, price_per_kg=None, auction_total=None, total_value=None, individual_prices=None):
    """
    Register a sale for a given establishment.
    """
    print(f'\n{establishment} is trying to register a sale on {sale_date}\n')
    print(f'Sheep list: {sheeps}| Sale type: {sale_type} | Total weight: {total_weight} kg | Meat value: {price_per_kg} us$/kg | Auction value: {auction_total} us$ | Total: {total_value} us$\n')
    
    value = auction_total if sale_type == 'auction' else total_value
    meat_value = price_per_kg if sale_type == 'slaughterhouse' else None
    print(f"Individual prices received: {individual_prices}")
    
    sheep_list = [sheep for sheep in sheeps if get_sheep(id=sheep.id)]
    
    try:
        sale = Venta.objects.create(
            sale_date=sale_date,
            total_weight=total_weight,
            meat_value=meat_value,
            total_value=value,
            establishment=establishment,
            sale_type=sale_type
        )

        if sale_type == 'individual' and individual_prices:
            for item in individual_prices:
                sheep_id = int(item.get("animal_id"))
                sale_price = item.get("sale_price")
                print(f"Sheep ID: {sheep_id} | Price: {sale_price}")
                
                for sheep in sheep_list:
                    print(f"Verifying sheep in list: ID {sheep.id}")
                    if sheep.id == sheep_id:
                        sheep.individual_sale_value = sale_price
                        sheep.save()
                        print(f"Sheep {sheep.id} updated with sale price: {sheep.individual_sale_value}")
            
        sale.sheep.set(sheep_list)
    
    except IntegrityError:
        return None
        
    return sale





    

def sale_information(request)->dict:
    """
    Returns a summary of the sales information for an establishment.

    The summary includes the quantity and total value of sales, categorized by sale type.

    Args:
        request (HttpRequest): The HTTP request containing the user information.

    Returns:
        dict: A dictionary containing:
            - total_sold (int): Total number of sales.
            - total_sales_value (float): Total value of sales.
            - auction_sales_count (int): Number of 'auction' sales.
            - slaughterhouse_sales_count (int): Number of 'slaughterhouse' sales.
            - individual_sales_count (int): Number of 'individual' sales.
            - donation_count (int): Number of 'donation' sales.
            - total_auction_sales (float): Total value of 'auction' sales.
            - total_slaughterhouse_sales (float): Total value of 'slaughterhouse' sales.
            - total_individual_sales (float): Total value of 'individual' sales.
            - total_donations (float): Total value of 'donation' sales.
    """
     # Get sales count by type
    auction_sales_count = int(Venta.objects.filter(sale_type='auction', establishment=request.user).count())
    slaughterhouse_sales_count = int(Venta.objects.filter(sale_type='slaughterhouse', establishment=request.user).count())
    individual_sales_count = int(Venta.objects.filter(sale_type='individual', establishment=request.user).count())
    donation_count = int(Venta.objects.filter(sale_type='donation', establishment=request.user).count())

    # Get monetary totals by type
    total_auction_sales = Venta.objects.filter(establishment=request.user, sale_type='auction').aggregate(Sum('total_value'))['total_value__sum'] or 0
    total_slaughterhouse_sales = Venta.objects.filter(establishment=request.user, sale_type='slaughterhouse').aggregate(Sum('total_value'))['total_value__sum'] or 0
    total_individual_sales = Venta.objects.filter(establishment=request.user, sale_type='individual').aggregate(Sum('total_value'))['total_value__sum'] or 0
    total_donations = Venta.objects.filter(establishment=request.user, sale_type='donation').aggregate(Sum('total_value'))['total_value__sum'] or 0

    # General totals
    total_sales_count = auction_sales_count + slaughterhouse_sales_count + individual_sales_count + donation_count
    total_sales_value = total_auction_sales + total_slaughterhouse_sales + total_individual_sales + total_donations

    sales_summary = {
        'total_sold': total_sales_count,
        'total_sales_value': total_sales_value,
        'auction_sales_count': auction_sales_count,
        'slaughterhouse_sales_count': slaughterhouse_sales_count,
        'individual_sales_count': individual_sales_count,
        'donation_count': donation_count,
        'total_auction_sales': total_auction_sales,
        'total_slaughterhouse_sales': total_slaughterhouse_sales,
        'total_individual_sales': total_individual_sales,
        'total_donations': total_donations,
    }
    return sales_summary




