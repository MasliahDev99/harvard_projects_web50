from django.db import IntegrityError
from .models import User




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

