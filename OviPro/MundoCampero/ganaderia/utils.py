from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .models import User,Raza,CalificadorPureza,Oveja




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

def agregar_oveja(bu, rp, peso, raza_nombre, calificador_nombre, edad, fecha_nacimiento, sexo, padre=None, madre=None, observaciones=None, nombre=None):
    try:
        # Buscar la raza por su nombre
        raza = obtener_raza(raza_nombre)
    except ObjectDoesNotExist:
        raise ValueError(f"La raza '{raza_nombre}' no existe.")
    
    try:
        # Buscar el calificador por su nombre
        calificador = CalificadorPureza.objects.get(nombre=calificador_nombre)
    except ObjectDoesNotExist:
        raise ValueError(f"El calificador '{calificador_nombre}' no existe.")

    # Crear la oveja
    nueva_oveja = Oveja(
        BU=bu,
        RP=rp,
        nombre=nombre,
        peso=peso,
        raza=raza,  # Usamos la instancia de Raza
        edad=edad,
        fechaNacimiento=fecha_nacimiento,
        sexo=sexo,
        calificador_pureza=calificador,  # Usamos la instancia de CalificadorPureza
        oveja_padre=padre,  # Si padre es None, queda vacío
        oveja_madre=madre,  # Si madre es None, queda vacío
        observaciones=observaciones,

    )
    nueva_oveja.save()

    return nueva_oveja

def obtener_todas_las_ovejas():
    return Oveja.objects.all()

def obtener_todos_tipos_cantidad():
    corderos = Oveja.objects.filter(edad__lte=6, sexo='Macho').count()
    corderas = Oveja.objects.filter(edad__lte=6, sexo='Hembra').count()
    borregos = Oveja.objects.filter(edad__gte=7, edad__lte=12, sexo='Macho').count()
    borregas = Oveja.objects.filter(edad__gte=7, edad__lte=12, sexo='Hembra').count()  # Corregido 'tte' a 'lte'

    # Borregos adultos y borregas adultas
    borregos_adultos = Oveja.objects.filter(edad__gt=12, sexo='Macho').count()
    borregas_adultas = Oveja.objects.filter(edad__gt=12, sexo='Hembra').count()  # Corregido 'borregos_adultos' a 'borregas_adultas'

    total_ovejas = Oveja.objects.all().count()

    return corderos, corderas, borregos, borregas, borregos_adultos, borregas_adultas, total_ovejas