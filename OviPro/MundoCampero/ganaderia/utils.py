from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Raza,CalificadorPureza,Oveja,Venta
from datetime import date,datetime
from django.db.models import Sum


def crear_establecimiento(username,RUT,email,password):
    if existe_establecimiento(RUT):
        raise IntegrityError("El RUT ingresado ya existe.")
    
    nuevo_establecimiento = User(username=username,RUT=RUT,email=email,password=password)
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
    return Oveja.objects.filter(establecimiento = request.user)

def obtener_todos_tipos_cantidad(request):
    user_ovejas = Oveja.objects.filter(establecimiento=request.user)
    
    corderos = user_ovejas.filter(edad__lte=6, sexo='Macho').count()
    corderas = user_ovejas.filter(edad__lte=6, sexo='Hembra').count()
    borregos = user_ovejas.filter(edad__gt=6, edad__lte=12, sexo='Macho').count()
    borregas = user_ovejas.filter(edad__gt=6, edad__lte=12, sexo='Hembra').count()
    
    carneros = user_ovejas.filter(edad__gt=12, sexo='Macho').count()
    ovejas = user_ovejas.filter(edad__gt=12, sexo='Hembra').count()
    
    total_ovejas = user_ovejas.count()

    return corderos, corderas, borregos, borregas, carneros, ovejas, total_ovejas


def obtener_oveja(rp=None, bu=None, id=None):
    try:
        if rp:
            return Oveja.objects.get(RP=rp)
        if bu:
            return Oveja.objects.get(BU=bu)
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

def set_padre_madre_externo(padre_externo,madre_externo,oveja):
    # seteamos los valores de padre externo y madre a una oveja
    oveja.rp_padre_externo = padre_externo
    oveja.rp_madre_externo = madre_externo
    oveja.save()


def validar_padre_madre(oveja_padre, oveja_madre,RP):
    """
        Valida que el padre y madre no sean iguales y que la oveja no sea su propio padre o madre

        futuro : usar la api de ARU para esten registrados en la base de datos de ARU
    """
    if oveja_padre == oveja_madre or RP in [oveja_padre, oveja_madre]:
            return None, None
    
    #buscamos en la base de datos de ovejas
    padre = obtener_oveja(rp=oveja_padre)
    madre = obtener_oveja(rp=oveja_madre)

    if not padre or not madre:
        #si no lo encontro en la base de datos, se busca en la base de datos de ARU
        # y registra los padres  como padre externo y madre externo

        return None, None

    return padre, madre


 


def agregar_oveja(request):
    # Capturamos los datos del formulario de registro de ovejas
    BU = request.POST.get('BU')
    RP = request.POST.get('RP')
    peso = request.POST.get('peso')
    raza = request.POST.get('raza')
    fecha_nacimiento = request.POST.get('fecha_nacimiento')
    sexo = request.POST.get('sexo')
    calificador_pureza = request.POST.get('calificador_pureza')
    observacion_seleccionada = request.POST.get('obs') == 'on'
    oveja_comprada = request.POST.get('purchased') == 'on'
    # Seteamos los valores de observaciones, oveja_padre y oveja_madre en None
    observaciones = None
    establecimiento = request.user

    # Verificamos si existe la oveja en la base de datos
    if existe_oveja(RP=RP, BU=BU):
        return None, "Ya existe una oveja con ese RP o BU"

    # Seteamos los valores de rp_padre_externo y rp_madre_externo en None si no se seleccionó la oveja comprada
    rp_padre_externo = request.POST.get('rp_padre_externo') if oveja_comprada else None
    rp_madre_externo = request.POST.get('rp_madre_externo') if oveja_comprada else None

    oveja_padre, oveja_madre = None, None  # Aquí se soluciona el error

    if not oveja_comprada:
        oveja_padre = request.POST.get('oveja_padre')
        oveja_madre = request.POST.get('oveja_madre')
        # Validamos que oveja padre y madre existan y validamos que madre y padre no sean iguales
        oveja_padre, oveja_madre = validar_padre_madre(oveja_padre, oveja_madre, RP)
        if oveja_padre is None and oveja_madre is None:
            # Si no hay padres, no mostramos un error por el momento
            pass
        elif not oveja_padre or not oveja_madre:
            return None, "Oveja padre o madre no encontrada"

    fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
    if fecha_nacimiento > date.today():
        return None, "La fecha de nacimiento no puede ser mayor a la fecha actual"
    
    # Calculamos la edad de la oveja
    edad = calcular_edad_por_fecha_nacimiento(fecha_nacimiento)

    # Capturamos el valor booleano de observaciones
    observaciones = request.POST.get('observaciones') if observacion_seleccionada else None
    
    # Obtenemos las instancias de raza y calificador de pureza
    try:
        raza = obtener_raza(raza)
        calificador_pureza = obtener_calificador(calificador_pureza)

    except ObjectDoesNotExist:
        return None, "Raza o calificador de pureza no encontrado"
   
    try:
        nueva_oveja = Oveja.objects.create(
            BU=BU,
            RP=RP,
            peso=peso,
            raza=raza,
            edad=edad,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            calificador_pureza=calificador_pureza,
            observaciones=observaciones,
            oveja_padre=oveja_padre,
            oveja_madre=oveja_madre,
            establecimiento=establecimiento,
            rp_padre_externo=rp_padre_externo,
            rp_madre_externo=rp_madre_externo,
        )
        return nueva_oveja, "Oveja registrada correctamente"
    except IntegrityError as e:
        return None, f"Error al registrar la oveja: {str(e)}"




# ventas, metodo de ventas


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