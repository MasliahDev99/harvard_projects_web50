from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Raza,CalificadorPureza,Oveja,Venta
from datetime import date,datetime
from django.db.models import Sum


from django.template.loader import get_template
import pdfkit

"""
    Purpose:
    This file serves as a central repository for utility functions used throughout 
    the project. These utility functions provide reusable logic for various operations, 
    such as database queries, validations, and data processing, ensuring a clean and maintainable 
    codebase by reducing redundancy in views or other modules.


"""


def crear_establecimiento(username,RUT,codigo_criador_ARU,email,password):
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
    if existe_establecimiento(RUT):
        raise IntegrityError("El RUT ingresado ya existe.")
    
    nuevo_establecimiento = User(username=username,RUT=RUT,email=email,password=password,registro_ARU_criador = codigo_criador_ARU)
    nuevo_establecimiento.set_password(password) # ciframos la contrasenia
    nuevo_establecimiento.save()

    return nuevo_establecimiento

# verifica si existe el rut rut
def existe_establecimiento(RUT):
    """
        Checks if an establishment exists in the database based on its RUT.

        Args:
            RUT (int): Identification Code to check.

        Returns:
            bool: True if the establishment exists, False otherwise.
    """
    return User.objects.filter(RUT=RUT).exists()


#obtenemos la referencia del establecimiento por el id o su Rut
def obtener_establecimiento_por_id(id=None,RUT=None):
    """
    Retrieves an establishment (user) by its ID or RUT.

    Args:
        id (int, optional): The unique ID of the establishment.
        RUT (int, optional): The unique RUT of the establishment.

    Returns:
        User: The corresponding user instance if found, otherwise None.
    """
    if id:
        return User.objects.get(id=id)
    if RUT:
        return User.objects.get(RUT=RUT)
    return None

def obtener_nombre_con_rut(RUT):
    """
    Retrieves the name of an establishment by its RUT.

    Args:
        RUT (int): Identification Code of the establishment.

    Returns:
        str: The name of the establishment if found, otherwise None.
    """
    if existe_establecimiento(RUT):
        establecimiento = User.objects.get(RUT=RUT)
        return establecimiento.username
    return None

# utils -> raza y calificadores de pureza

def obtener_raza(raza_nombre):
    """
    Retrieves a breed instance by its name.

    Args:
        raza_nombre (str): Name of the breed.

    Returns:
        Raza: The corresponding breed instance.

    Raises:
        ObjectDoesNotExist: If the breed is not found.
    """
    return Raza.objects.get(nombre=raza_nombre)

def obtener_calificador(calificador_nombre):
    """
    Retrieves a purity qualifier by its name.

    Args:
        calificador_nombre (str): Name of the qualifier.

    Returns:
        CalificadorPureza: The corresponding purity qualifier instance.

    Raises:
        ObjectDoesNotExist: If the qualifier is not found.
    """
    return CalificadorPureza.objects.get(nombre = calificador_nombre)


# utils -> ovejas relacion establecimiento


def obtener_todas_las_ovejas(request):
    """
    Retrieves all active sheep associated with the logged-in user's establishment.

    Args:
        request (HttpRequest): The current HTTP request containing user information.

    Returns:
        QuerySet: A list of active sheep for the user's establishment.
    """
    return Oveja.objects.filter(establecimiento = request.user,estado='activa')

def obtener_todos_tipos_cantidad(request):
    """
    Retrieves the count of all sheep categorized by type and age group.

    Args:
        request (HttpRequest): The current HTTP request containing user information.

    Returns:
        tuple: Counts for corderos, corderas, borregos, borregas, carneros, ovejas, and total sheep.
    """
    user_ovejas = Oveja.objects.filter(establecimiento=request.user,estado='activa')
    
    corderos = user_ovejas.filter(edad__lte=6, sexo='Macho').count()
    corderas = user_ovejas.filter(edad__lte=6, sexo='Hembra').count()
    borregos = user_ovejas.filter(edad__gt=6, edad__lte=12, sexo='Macho').count()
    borregas = user_ovejas.filter(edad__gt=6, edad__lte=12, sexo='Hembra').count()
    
    carneros = user_ovejas.filter(edad__gt=12, sexo='Macho').count()
    ovejas = user_ovejas.filter(edad__gt=12, sexo='Hembra').count()
    
    total_ovejas = user_ovejas.count()

    return corderos, corderas, borregos, borregas, carneros, ovejas, total_ovejas


def obtener_oveja(rp=None, id=None):
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
    
def existe_oveja(RP=None, BU=None):
    """
    Checks if a sheep exists in the database based on its RP or BU.

    Args:
        RP (str, optional): The RP of the sheep.
        BU (str, optional): The BU (Internal Identifier) of the sheep.

    Returns:
        bool: True if a sheep with the given RP or BU exists, False otherwise.
    """
    if RP and Oveja.objects.filter(RP=RP).exists():
        return True
    if BU and Oveja.objects.filter(BU=BU).exists():
        return True
    return False



def calcular_edad_por_fecha_nacimiento(fecha_nacimiento):
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

def obtener_padre_madre(rp_padre, rp_madre):
    """
    Retrieves instances of the father and mother sheep if they exist.

    Args:
        rp_padre (int): RP of the father.
        rp_madre (int): RP of the mother.

    Returns:
        tuple: Instances of the father and mother sheep, or None if not found.
    """
    padre = Oveja.objects.filter(rp=rp_padre).first() if rp_padre else None
    madre = Oveja.objects.filter(rp=rp_madre).first() if rp_madre else None
    return padre, madre




    
def validar_padre_madre(oveja_padre, oveja_madre, RP, establecimiento):
    """
    Validates that the father and mother are not the same and that the sheep is not its own parent.

    Args:
        oveja_padre (int): RP of the father.
        oveja_madre (int): RP of the mother.
        RP (int): RP of the sheep being registered.
        establecimiento: The establishment to which the sheep belongs.

    Returns:
        list: A list of validation errors, or an empty list if valid.
    """
    errores = []

    # Verificar si padre y madre son iguales
    if oveja_padre == oveja_madre:
        errores.append("El padre y la madre no pueden ser el mismo animal.")

    # Verificar si el ovino es su propio padre o madre
    if RP in [oveja_padre, oveja_madre]:
        errores.append("El ovino no puede ser su propio padre o madre.")

    

    if errores:
        return None, None, errores

    return []

def existe_nombre(nombre,establecimiento):
    return Oveja.objects.filter(nombre__iexact=nombre,establecimiento=establecimiento).exists()

def generar_nombre_unico():
    """
    Generates a unique name using a UUID.

    Returns:
        str: A unique name.
    """
    import uuid
    return f"SinNombre-{uuid.uuid4().hex[:8]}" 


def existe_establecimiento(nombre):
    return Oveja.objects.filter(nombre__iexact=nombre).exists() 


def validar_fecha_nacimiento(fecha_nacimiento):
    """
    Validates that a given birth date is not in the future.

    Args:
        fecha_nacimiento (date): Birth date to validate.

    Returns:
        str or None: An error message if invalid, or None if valid.
    """
    if fecha_nacimiento > date.today():
        return "La fecha de nacimiento no puede ser futura."
    return None

def obtener_datos_formulario_ov(request):
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




def agregar_oveja(request):
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
    errores = []

    # Capturar datos del formulario
    BU, RP, nombre, peso, raza, fecha_nacimiento, sexo, calificador_pureza, observacion_seleccionada, oveja_comprada = obtener_datos_formulario_ov(request)
    observaciones = None
    establecimiento = request.user

    # Verificar si la oveja ya existe por RP
    if RP and existe_oveja(RP=RP):
        errores.append(f"Ya existe una oveja con RP {RP}.")

    oveja_padre, oveja_madre = None, None

    # Validación para raza 'pedigri'
    if raza == 'pedigri':
        oveja_padre = request.POST.get('oveja_padre')
        oveja_madre = request.POST.get('oveja_madre')
        if not RP:
            errores.append("El campo RP es obligatorio para pureza pedigri.")
        # Validar los padres
        oveja_padre, oveja_madre, errores_validacion = validar_padre_madre(oveja_padre, oveja_madre, RP)
        if errores_validacion:
            errores.extend(errores_validacion)

    # Validar oveja comprada
    origen = None
    if oveja_comprada:
        origen = request.POST.get('origen')
        if not origen:
            origen = 'No especificado.'

    # Validar fecha de nacimiento
    try:
        fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
        if fecha_nacimiento > date.today():
            errores.append("La fecha de nacimiento no puede ser mayor a la fecha actual.")
    except ValueError:
        errores.append("Formato de fecha no válido. Use el formato YYYY-MM-DD.")

    # Si no hay errores hasta ahora, calcular la edad
    if not errores:
        edad = calcular_edad_por_fecha_nacimiento(fecha_nacimiento)

    # Obtener observaciones
    observaciones = request.POST.get('observaciones') if observacion_seleccionada else None

    # Obtener raza y calificador de pureza
    try:
        raza = obtener_raza(raza)
        calificador_pureza = obtener_calificador(calificador_pureza)
    except ObjectDoesNotExist:
        errores.append("Raza o calificador de pureza no encontrado.")

    # si no se ingreso nombre, le agregamos uno  por defecto y si ingreso revisamos que no exista
    if not nombre:
        nombre = generar_nombre_unico()
    else:
        if existe_nombre(nombre=nombre, establecimiento=establecimiento):
            errores.append(f"Ya existe un ovino registrado con ese nombre: {nombre} en este establecimiento.")

    # Si hay errores, retornar antes de crear la oveja
    if errores:
        return None, errores

    # Intentar crear la oveja
    try:
        
        nueva_oveja = Oveja.objects.create(
            BU=BU,
            RP=RP,
            nombre=nombre,
            peso=peso,
            raza=raza,
            edad=edad,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            calificador_pureza=calificador_pureza,
            observaciones=observaciones,
            padre=oveja_padre,
            madre=oveja_madre,
            establecimiento=establecimiento,
            establecimiento_origen=origen,
        )
        return nueva_oveja, ["Oveja registrada correctamente"]
    except IntegrityError as e:
        return None, [f"Error al registrar la oveja: {str(e)}"]


def set_rp(nuevo_RP: str, id_oveja: int):
    """
    Updates the RP of a sheep with a new identifier.

    Args:
        nuevo_RP (str): The new RP to assign.
        id_oveja (int): The ID of the sheep to update.

    Returns:
        tuple: A boolean indicating success and a list with a message:
            - (True, [message]) if the RP is successfully updated.
            - (False, [error message]) if the RP already exists or the sheep does not exist.
    """
    try:
        oveja = Oveja.objects.get(id=id_oveja)
    except Oveja.DoesNotExist:
        return False, [f"No se encontró ninguna oveja con el ID {id_oveja}."]
    
    if Oveja.objects.filter(RP=nuevo_RP).exists():
        return False, [f"Error: Ya existe un ovino con RP: {nuevo_RP} ."]
    
    oveja.RP = nuevo_RP
    oveja.save()
    return True, [f"RP actualizado correctamente a {nuevo_RP} para el ovino con ID {id_oveja}."]


    



# ventas, metodo de ventas

def registrar_venta( establecimiento,lista_ovejas,tipo_venta, fecha_venta, peso_total=None ,precio_kg=None, remate_total=None, valor_total=None):
    """
    Registers a sale for a given establishment.

    Args:
        establecimiento (User): The establishment responsible for the sale.
        lista_ovejas (list): List of sheep involved in the sale.
        tipo_venta (str): The type of sale ('remate', 'frigorifico', 'individual', 'donacion').
        fecha_venta (datetime): The date of the sale.
        peso_total (float, optional): Total weight of the sheep in kilograms.
        precio_kg (float, optional): Price per kilogram (used for 'frigorifico' sales).
        remate_total (float, optional): Total value for 'remate' sales.
        valor_total (float, optional): Total sale value for other types of sales.

    Returns:
        Venta: The registered sale instance if successful.
        None: If an `IntegrityError` occurs during registration.
    """

    print(f'\n{establecimiento} esta intentando registrar una venta {fecha_venta}\n')
    print(f'Lista de ovejas {lista_ovejas}| tipo de venta: {tipo_venta} | peso total {peso_total} kg | valor de carne {precio_kg} us$/kg | valor de remate {remate_total} us$ | total {valor_total} us$\n')
    valor = remate_total if tipo_venta == 'remate' else valor_total
    valor_carne = precio_kg if tipo_venta == 'frigorifico' else None

    #actualizamos la lista de las ovejas con las instancias de las ovejas utilizando lista comprension
    lista_ovejas = [oveja for oveja in lista_ovejas if obtener_oveja(rp=oveja.RP)] 
   
    try:
        venta = Venta.objects.create(
            fecha_venta=fecha_venta,
            peso_total = peso_total,
            valor_carne=valor_carne,
            valor=valor,
            establecimiento=establecimiento,
            tipo_venta=tipo_venta
        )
    except IntegrityError:
        return None
        
    return venta


def informacion_de_ventas(request)->dict:
    """
    Returns a summary of the sales information for an establishment.

    The summary includes the quantity and total value of sales, categorized by sale type.

    Args:
        request (HttpRequest): The HTTP request containing the user information.

    Returns:
        dict: A dictionary containing:
            - cantidad_vendida (int): Total number of sales.
            - total_ventas (float): Total value of sales.
            - cantidad_ventas_por_remate (int): Number of 'remate' sales.
            - cantidad_ventas_por_frigorifico (int): Number of 'frigorifico' sales.
            - cantidad_ventas_por_individual (int): Number of 'individual' sales.
            - cantidad_donaciones (int): Number of 'donation' sales.
            - total_ventas_remate (float): Total value of 'remate' sales.
            - total_ventas_frigorifico (float): Total value of 'frigorifico' sales.
            - total_ventas_individual (float): Total value of 'individual' sales.
            - total_donaciones (float): Total value of 'donation' sales.
    """
    # Obtenemos la cantidad de ventas por cada  tipo de venta 
    cantidad_ventas_por_remate = int(Venta.objects.filter(tipo_venta='remate', establecimiento=request.user).count())
    cantidad_ventas_por_frigorifico = int(Venta.objects.filter(tipo_venta='frigorifico', establecimiento=request.user).count())
    cantidad_ventas_por_individual = int(Venta.objects.filter(tipo_venta='individual', establecimiento=request.user).count())
    cantidad_donaciones = int(Venta.objects.filter(tipo_venta='donacion', establecimiento=request.user).count())
    # obtenemos las ventas del establecimiento de cada tipo de venta
    # seteadas en 0 todas

      # Totales monetarios por cada tipo
    total_ventas_remate = Venta.objects.filter(establecimiento=request.user, tipo_venta='remate').aggregate(Sum('valor'))['valor__sum'] or 0
    total_ventas_frigorifico = Venta.objects.filter(establecimiento=request.user, tipo_venta='frigorifico').aggregate(Sum('valor'))['valor__sum'] or 0
    total_ventas_individual = Venta.objects.filter(establecimiento=request.user, tipo_venta='individual').aggregate(Sum('valor'))['valor__sum'] or 0
    total_donaciones = Venta.objects.filter(establecimiento=request.user, tipo_venta='donacion').aggregate(Sum('valor'))['valor__sum'] or 0
     
    # Total general
    cantidad_vendida = cantidad_ventas_por_remate + cantidad_ventas_por_frigorifico + cantidad_ventas_por_individual + cantidad_donaciones
    total_ventas = total_ventas_remate + total_ventas_frigorifico + total_ventas_individual + total_donaciones
  
    resumen_ventas = {
        'cantidad_vendida': cantidad_vendida,
        'total_ventas': total_ventas,
        'cantidad_ventas_por_remate': cantidad_ventas_por_remate,
        'cantidad_ventas_por_frigorifico': cantidad_ventas_por_frigorifico,
        'cantidad_ventas_por_individual': cantidad_ventas_por_individual,
        'cantidad_donaciones': cantidad_donaciones,
        'total_ventas_remate': total_ventas_remate,
        'total_ventas_frigorifico': total_ventas_frigorifico,
        'total_ventas_individual': total_ventas_individual,
        'total_donaciones': total_donaciones,
    }
    return resumen_ventas



