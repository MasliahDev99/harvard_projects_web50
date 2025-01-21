from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Raza,CalificadorPureza,Oveja,Venta
from datetime import date,datetime
from django.db.models import Sum


from django.template.loader import get_template
import pdfkit

"""
    Este archivo tiene de finalidad tener metodos utiles para utilizarlas en views.py

    metodods:
        -crear_establecimiento()
        -existe_establecimiento()
        -obtener_establecimiento_por_id()
        -obtener_nombre_con_RUT()
        -obtener_raza()
        -obtener_todas_las_ovejas()
        -obtener_todo_tipo_cantidad()
        -obtener_oveja()
        -existe_oveja()
        -calcular_edad_por_fecha_nacimiento()
        -obtener_padre_madre()
        ...




"""


def crear_establecimiento(username,RUT,codigo_criador_ARU,email,password):
    if existe_establecimiento(RUT):
        raise IntegrityError("El RUT ingresado ya existe.")
    
    nuevo_establecimiento = User(username=username,RUT=RUT,email=email,password=password,registro_ARU_criador = codigo_criador_ARU)
    nuevo_establecimiento.set_password(password) # ciframos la contrasenia
    nuevo_establecimiento.save()

    return nuevo_establecimiento

# verifica si existe el rut rut
def existe_establecimiento(RUT):
    return User.objects.filter(RUT=RUT).exists()


#obtenemos la referencia del establecimiento por el id o su Rut
def obtener_establecimiento_por_id(id=None,RUT=None):
    if id:
        return User.objects.get(id=id)
    if RUT:
        return User.objects.get(RUT=RUT)
    return None

def obtener_nombre_con_rut(RUT):
    if existe_establecimiento(RUT):
        establecimiento = User.objects.get(RUT=RUT)
        return establecimiento.username
    return None

# utils -> raza y calificadores de pureza

def obtener_raza(raza_nombre):
  
    return Raza.objects.get(nombre=raza_nombre)

def obtener_calificador(calificador_nombre):
   
    return CalificadorPureza.objects.get(nombre = calificador_nombre)


# utils -> ovejas relacion establecimiento


def obtener_todas_las_ovejas(request):
    """
        Retorna la lista de todas las ovejas activas del establecimiento
    """
    return Oveja.objects.filter(establecimiento = request.user,estado='activa')

def obtener_todos_tipos_cantidad(request):
    """
        retorna todos los ovinos con su cantidad correspondiente a la edad y esten activas
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
    Verifica si existe una oveja con el mismo RP o BU en la base de datos.
    """
    if RP and Oveja.objects.filter(RP=RP).exists():
        return True
    if BU and Oveja.objects.filter(BU=BU).exists():
        return True
    return False



def calcular_edad_por_fecha_nacimiento(fecha_nacimiento):
    """
    Calcula la edad en meses a partir de la fecha de nacimiento.
    :param fecha_nacimiento: Fecha de nacimiento en formato 'dd/mm/yyyy' como string.
    :return: Edad en meses como entero.
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
    Retorna las instancias de padre y madre si existen, o None si no se encuentran.
    """
    padre = Oveja.objects.filter(rp=rp_padre).first() if rp_padre else None
    madre = Oveja.objects.filter(rp=rp_madre).first() if rp_madre else None
    return padre, madre




    
def validar_padre_madre(oveja_padre, oveja_madre, RP, establecimiento):
    """
    Valida que el padre y madre no sean iguales y que la oveja no sea su propio padre o madre.
    Registra los padres como ovejas externas si no están en la base de datos.
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
    import uuid
    return f"SinNombre-{uuid.uuid4().hex[:8]}" 


def existe_establecimiento(nombre):
    return Oveja.objects.filter(nombre__iexact=nombre).exists() 


def validar_fecha_nacimiento(fecha_nacimiento):
    if fecha_nacimiento > date.today():
        return "La fecha de nacimiento no puede ser futura."
    return None

def obtener_datos_formulario_ov(request):
    """
    Captura los datos enviados desde el formulario de registro de ovinos y los retorna.
    Si algunos campos no están presentes, establece valores predeterminados como `None` o `False`.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene los datos del formulario.

    Returns:
        tuple: Valores capturados del formulario.
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
        Devuelve la instancia de la venta registrada segun su tipo

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
        Retorna un diccionario con la informacion de ventas del establecimiento

        cantidad_vendida: cantidad de ventas realizadas
        total_ventas: total de ventas realizadas

        cantodad_ventas_por_remate: cantidad de ventas por remate
        cantidad_ventas_por_frigorifico: cantidad de ventas por frigorifico
        cantidad_ventas_por_individual: cantidad de ventas por individual
        cantidad_donaciones: cantidad de donaciones realizadas

        total_ventas_por_remate: total de ventas por remate
        total_ventas_por_frigorifico: total de ventas por frigorifico
        total_ventas_por_individual: total de ventas por individual
        total_donaciones: total de donaciones realizadas

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



