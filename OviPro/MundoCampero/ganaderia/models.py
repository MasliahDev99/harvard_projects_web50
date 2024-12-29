from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

"""
* Razas(nombre)

*CalificadorPureza(nombre)

* Establecimiento(Rut,email, contrasenia)
* Ovejas(BU,RP,nombre,peso,Raza,edad,fechaNacimiento,Sexo,Calificador_Pureza,Observaciones,Oveja_padre,Oveja_Madre)
* Ventas(Ovejas,FechaVenta,valor,Tipo_venta)
*Planteleta(Oveja,Tipo_plantel)
*Genealogia(Oveja,Oveja_padre,Oveja_madre)

"""
class Raza(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

class CalificadorPureza(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

#User => Establecimiento
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    RUT = models.IntegerField(unique=True, null=True,blank=True ,validators=[MinValueValidator(1000000), MaxValueValidator(999999999999)])
    telefono = models.IntegerField(null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

