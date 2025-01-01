from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Raza,CalificadorPureza,Oveja
from datetime import date,datetime



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
    return CalificadorPureza.objects.get(calificador_nombre)


# utils -> ovejas relacion establecimiento


def obtener_todas_las_ovejas(request):
    return Oveja.objects.filter(establecimiento = request.user)

def obtener_todos_tipos_cantidad(request):
    user_ovejas = Oveja.objects.filter(establecimiento=request.user)
    
    corderos = user_ovejas.filter(edad__lte=6, sexo='Macho').count()
    corderas = user_ovejas.filter(edad__lte=6, sexo='Hembra').count()
    borregos = user_ovejas.filter(edad__gte=7, edad__lte=12, sexo='Macho').count()
    borregas = user_ovejas.filter(edad__gte=7, edad__lte=12, sexo='Hembra').count()
    
    borregos_adultos = user_ovejas.filter(edad__gt=12, sexo='Macho').count()
    borregas_adultas = user_ovejas.filter(edad__gt=12, sexo='Hembra').count()
    
    total_ovejas = user_ovejas.count()

    return corderos, corderas, borregos, borregas, borregos_adultos, borregas_adultas, total_ovejas


# obtener oveja por rp,bu o id
def obtener_oveja(rp=None,bu=None,id=None):
    if rp:
        return Oveja.objects.get(rp=rp)
    if bu:
        return Oveja.objects.get(bu=bu)
    if id:
        return Oveja.objects.get(id=id)
    else:
        return None
    
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




 


def agregar_oveja(request):
    #capturamos los datos del formulario de registro de ovejas
    BU = request.POST.get('BU')
    RP = request.POST.get('RP')
    peso = request.POST.get('peso')
    raza = request.POST.get('raza')
    edad = request.POST.get('edad')
    fecha_nacimiento = request.POST.get('fecha_nacimiento') # ya esta formateada
    sexo = request.POST.get('sexo')
    calificador_pureza = request.POST.get('calificador_pureza')

    #seteamos los valores de observaciones,oveja_padre y oveja_madre en null
    observaciones = None
    oveja_padre = None
    oveja_madre = None
    
    establecimiento = request.user


    #verificamos si existe la oveja en la base de datos

    if existe_oveja(RP=RP,BU=BU):
        return None
    


    #capturamos el valor booleano de oveja comprada
    oveja_comprada = True if request.POST.get('purchased') == 'on' else False
    #capturamos el valor booleano de observaciones
    observacion_seleccionada = True if request.POST.get('obs') == 'on' else False

    #seteamos los valores de rp padre y madre externos en null
    rp_padre_externo = None
    rp_madre_externo = None


    # si el usuario selecciona oveja comprada capturamos los valores de rp padre y madre externos
    if oveja_comprada == 'on':
        rp_padre_externo = request.POST.get('rp_padre_externo')
        rp_madre_externo = request.POST.get('rp_madre_externo')
    else:
        # si no es oveja comprada entonces capturamos los valores de rp padre y madre internos
        oveja_padre = request.POST.get('oveja_padre')
        oveja_madre = request.POST.get('oveja_madre')

        # verificamos que existan los padres en la base de datos y que no sean la misma oveja
        if oveja_padre == oveja_madre:
            return None
        if RP == oveja_padre or RP == oveja_madre:
            return None
        # si existen los padres en la base de datos entonces obtenemos las instancias
        if Oveja.objects.get(RP=oveja_padre) and Oveja.objects.get(RP=oveja_madre):
            oveja_padre = obtener_oveja(rp=oveja_padre)
            oveja_madre = obtener_oveja(rp=oveja_madre)
        else:
            return None

    # si el usuario selecciona observaciones capturamos el valor de observaciones
    if observacion_seleccionada  == 'on':
        observaciones = request.POST.get('observaciones')

   

    #formateamos la fecha fecha_nacimiento y si es mayor a la fehca actual retorna None
    fecha_nacimiento = date.fromisoformat(fecha_nacimiento)
    if fecha_nacimiento > date.today():
        return None
    
    #calculamos la edad en meses
    edad = calcular_edad_por_fecha_nacimiento(fecha_nacimiento)


    #obtenemos las instancias de los objetos de raza
    try:
        raza = obtener_raza(raza)
        calificador_pureza = obtener_calificador(calificador_pureza)
    except ObjectDoesNotExist as e:
        return None
   
    #creamos

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
        return nueva_oveja
    except IntegrityError as e:
        return None
    
    


 


    
    
    


