from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Raza(models.Model):
    """
    Represents a breed of sheep.

    Attributes:
        id (int): The unique identifier for the breed.
        nombre (str): The name of the breed (e.g., 'Merino', 'Texel').
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre 

class CalificadorPureza(models.Model):
    """
    Represents the purity classification of sheep.

    Attributes:
        id (int): The unique identifier for the purity classifier.
        nombre (str): The name of the purity classification (e.g., 'pedigri', 'PO').
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre 

#User => Establecimiento
class User(AbstractUser):
    """
    Custom user model representing an establishment or farm.

    Attributes:
        id (int): The unique identifier for the user.
        RUT (int): The RUT (national ID) of the establishment (optional).
        telefono (int): Phone number of the establishment (optional).
        fecha_registro (datetime): Date and time of registration.
        registro_ARU_criador (int): The ARU (Rural Association of Uruguay) registration number (optional).
    """
    id = models.BigAutoField(primary_key=True)
    RUT = models.IntegerField(unique=True, null=True,blank=True ,validators=[MinValueValidator(1000000), MaxValueValidator(999999999999)])
    telefono = models.IntegerField(null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    # identificador de criador de ARU (asociacion rural del Uruguay)
    registro_ARU_criador = models.IntegerField(unique=True,null=True,blank=True)
    


class Oveja(models.Model):
    """
    Represents a sheep.

    Attributes:
        id (int): The unique identifier for the sheep.
        BU (str): The sheep's breed identification code (optional).
        RP (str): The sheep's registry number (unique).
        nombre (str): The sheep's name (optional).
        nombre_aux (str): Auxiliary name for the sheep (optional).
        peso (float): The weight of the sheep.
        raza (ForeignKey): The breed of the sheep (related to Raza).
        edad (int): The age of the sheep in months.
        fecha_nacimiento (date): The birth date of the sheep.
        sexo (str): The sex of the sheep ('Macho' for male, 'Hembra' for female).
        calificador_pureza (ForeignKey): The purity classification of the sheep (related to CalificadorPureza).
        observaciones (str): Any notes or observations about the sheep (optional).
        padre (str): The father’s registry number (optional).
        madre (str): The mother’s registry number (optional).
        establecimiento (ForeignKey): The establishment to which the sheep belongs (related to User).
        estado (str): The current state of the sheep ('activa', 'vendida', or 'muerta').
        valor_venta_ind (float): The price for individual sales (optional).
        fecha_muerte (date): The death date of the sheep (if applicable).
        establecimiento_origen (str): The establishment from which the sheep was purchased (optional).
    """
    id = models.AutoField(primary_key=True)
    BU = models.CharField(max_length=50,null=True, blank=True)
    RP = models.CharField(max_length=50,null=True, unique=True,blank=True)
    nombre = models.CharField(max_length=100,null=True,unique=True,blank=True)
    nombre_aux = models.CharField(max_length=100,null=True,blank=True)
    peso = models.FloatField()
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=(('Macho', 'Macho'), ('Hembra', 'Hembra')))
    calificador_pureza = models.ForeignKey(CalificadorPureza, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    # si el animal es pedigri necesitamos almacenar el rp de los padres
    padre = models.CharField(max_length=50, null=True, blank=True)
    madre = models.CharField(max_length=50, null=True, blank=True)

    establecimiento = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ovejas')
    estado = models.CharField(max_length=10, choices=[('activa','Activa'),('vendida', 'Vendida'),('muerta', 'Muerta')], default='activa')


    #para venta individual agregaremos un atributo de precio
    valor_venta_ind = models.FloatField(null=True,blank=True)

    # En caso que el estado del ovino sea "muerta" guardaremos la fecha de "muerte" 
    fecha_muerte = models.DateField(null=True, blank=True)  

    #si la oveja es comprada  guardamos el nombre del establecimiento
    establecimiento_origen = models.CharField(max_length=50,null=True,blank=True)

    def __str__(self):
        return self.nombre if self.nombre else self.RP
    
    def clasificar_edad(self):
        if self.edad <= 6:  # Cordero si tiene 6 meses o menos
            return 'Cordero' if self.sexo == 'Macho' else 'Cordera'
        elif self.edad <= 12:  # Borrego de 7 a 12 meses
            return 'Borrego' if self.sexo == 'Macho' else 'Borrega'
        else:  # Ovejas adultas (mayores de 12 meses)
            return 'Carnero' if self.sexo == 'Macho' else 'Oveja'
        

# modelo para tabla de ventas

class Venta(models.Model):
    """
    Represents a sale of sheep.

    Attributes:
        id (int): The unique identifier for the sale.
        ovejas (ManyToManyField): A list of sheep associated with the sale.
        fecha_venta (date): The date of the sale.
        peso_total (Decimal): The total weight of the sheep sold.
        valor_carne (float): The value of the meat (relevant for sales to frigorificos).
        valor (float): The total value of the sale.
        establecimiento (ForeignKey): The establishment making the sale (related to User).
        tipo_venta (str): The type of sale ('remate', 'individual', 'frigorifico', or 'donacion').
    """
    id = models.AutoField(primary_key=True)
    ovejas = models.ManyToManyField('Oveja', related_name='ventas', blank=True)  # Para soporte de venta por lote o individual
    fecha_venta = models.DateField()
    peso_total =  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_carne = models.FloatField(null=True, blank=True)  # Solo necesario para frigorífico
    valor = models.FloatField(default=0.0)
    establecimiento = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True ,related_name='ventas')
    # quiero gestionar la venta de ovinos de donacion y los tipos de venta en remate,individual o frigorifico
    tipo_venta = models.CharField(max_length=20, choices=[('remate', 'Remate'), ('individual', 'Individual'), ('frigorifico', 'Frigorífico'),('donacion', 'Donación')])

    def __str__(self):
        ovejas_nombres = ", ".join(oveja.nombre for oveja in self.ovejas.all())
        return f"Venta del {self.fecha_venta} - Tipo: {self.tipo_venta} - Ovejas: {ovejas_nombres}"
    


# Falta implementar el modelo de Planteleta 
"""
Planteleta(id,ovejas,nombre_plantel,)

"""
    
   

    
    
    
    



   