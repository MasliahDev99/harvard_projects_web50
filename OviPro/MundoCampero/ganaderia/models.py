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

    def __str__(self):
        return self.nombre 

class CalificadorPureza(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre 

#User => Establecimiento
class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    RUT = models.IntegerField(unique=True, null=True,blank=True ,validators=[MinValueValidator(1000000), MaxValueValidator(999999999999)])
    telefono = models.IntegerField(null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    


class Oveja(models.Model):
    id = models.AutoField(primary_key=True)
    BU = models.CharField(max_length=50, unique=True)
    RP = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100,null=True)
    peso = models.FloatField()
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=(('Macho', 'Macho'), ('Hembra', 'Hembra')))
    calificador_pureza = models.ForeignKey(CalificadorPureza, on_delete=models.SET_NULL, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    # si  la oveja a registrar tiene rp padre y madre internos a la tabla de ovejas
    oveja_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='hijos_padre')
    oveja_madre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='hijos_madre')


    establecimiento = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ovejas')  # Relación con el User (Establecimiento)
    

  
    ESTADOS = [
        ('activa', 'Activa'),
        ('vendida', 'Vendida'),
        ('muerta', 'Muerta'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activa')

    # si la oveja es comprada  entonces sus rp padre y madre son externos a la tabla de ovejas
    rp_padre_externo = models.CharField(max_length=50, null=True, blank=True)
    rp_madre_externo = models.CharField(max_length=50, null=True, blank=True)

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
    id = models.AutoField(primary_key=True)
    ovejas = models.ManyToManyField('Oveja', related_name='ventas', blank=True)  # Para soporte de venta por lote o individual
    fecha_venta = models.DateField()
    valor_carne = models.FloatField(null=True, blank=True)  # Solo necesario para frigorífico
    valor = models.FloatField(default=0.0)
    establecimiento = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True ,related_name='ventas')

   # quiero gestionar la venta de ovinos de donacion y los tipos de venta en remate,individual o frigorifico
    TIPOS_VENTA = [
        ('remate', 'Remate'), # valor de venta por subasta acordada
        ('individual', 'Individual'), # valor de venta acordada
        ('frigorifico', 'Frigorífico'), # formula -> valor_venta = valor_carne * kg 
        ('donacion', 'Donación'), # donacion valor 0
    ]
    tipo_venta = models.CharField(max_length=20, choices=TIPOS_VENTA)

    def __str__(self):
        ovejas_nombres = ", ".join(oveja.nombre for oveja in self.ovejas.all())
        return f"Venta del {self.fecha_venta} - Tipo: {self.tipo_venta} - Ovejas: {ovejas_nombres}"
    

    def calcular_valor_total(self):
        if self.tipo_venta == 'frigorifico' and self.valor_carne:
            self.valor_total = sum(oveja.peso * self.valor_carne for oveja in self.ovejas.all())
        elif self.tipo_venta == 'donacion':
            self.valor_total = 0.0
        elif self.tipo_venta in ['remate', 'individual']:
            self.valor_total = sum(oveja.valor_estimado for oveja in self.ovejas.all())
        self.save()
        return self.valor_total
    # ventas por lote o por unidad
    
    def venta_por_frigorifico(self,valor_carne):
        if self.tipo_venta == 'frigorifico':
            return self.oveja.peso * valor_carne
        
    def vender_lote_frigorifico(self,lista_ovejas:list,valor_carne)->float:
        total = 0.0
        #recorremos la lista de ovejas
        for oveja in lista_ovejas:
            # si la oveja existe y esta activa
            if Oveja.objects.filter(id=oveja.id).exists() and oveja.estado == 'activa':
                #acumulamos en total el valor del calculo del frigorifico
                total += oveja.peso * valor_carne
                #actualizamos el estado de la oveja
                oveja.estado = 'vendida'

        return total
    
    def aceptar_venta(self):
        # Cambiar estado de las ovejas a 'vendida'
        for oveja in self.ovejas.all():
            oveja.estado = 'vendida'
            oveja.save()
    
