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
        name (str): The name of the breed (e.g., 'Merino', 'Texel').
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name  

class CalificadorPureza(models.Model):
    """
    Represents the purity classification of sheep.

    Attributes:
        id (int): The unique identifier for the purity classifier.
        nombre (str): The name of the purity classification (e.g., 'pedigri', 'PO').
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name

#User => Establecimiento
class User(AbstractUser):
    """
    Custom user model representing an establishment or farm.

    Attributes:
        id (int): The unique identifier for the user.
        RUT (int): The RUT (national ID) of the establishment (optional).
        phone (int): Phone number of the establishment (optional).
        registration_date (datetime): Date and time of registration.
        ARU_bred_registration (int): The ARU (Rural Association of Uruguay) registration number (optional).
    """
    id = models.BigAutoField(primary_key=True)
    RUT = models.IntegerField(unique=True, null=True,blank=True ,validators=[MinValueValidator(1000000), MaxValueValidator(999999999999)])
    phone = models.IntegerField(null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    # identificador de criador de ARU (asociacion rural del Uruguay)
    ARU_bred_registration = models.IntegerField(unique=True,null=True,blank=True)
    


class Oveja(models.Model):
    """
    Represents a sheep.

    Attributes:
        id (int): The unique identifier for the sheep.
        BU (str): The sheep's breed identification code (optional).
        RP (str): The sheep's registry number (unique).
        name (str): The sheep's name (optional).
        auxiliary_name (str): Auxiliary name for the sheep (optional).
        weight (float): The weight of the sheep.
        breed (ForeignKey): The breed of the sheep (related to Raza).
        age (int): The age of the sheep in months.
        birth_date (date): The birth date of the sheep.
        sex (str): The sex of the sheep ('Male' for male, 'Female' for female).
        purity_qualifier (ForeignKey): The purity classification of the sheep (related to CalificadorPureza).
        notes (str): Any notes or observations about the sheep (optional).
        father (str): The father’s registry number (optional).
        mother (str): The mother’s registry number (optional).
        establishment (ForeignKey): The establishment to which the sheep belongs (related to User).
        status (str): The current state of the sheep ('active', 'sold', or 'dead').
        individual_sale_value (float): The price for individual sales (optional).
        death_date (date): The death date of the sheep (if applicable).
        origin_establishment (str): The establishment from which the sheep was purchased (optional).
    """
    
    id = models.AutoField(primary_key=True)
    BU = models.CharField(max_length=50, null=True, blank=True)
    RP = models.CharField(max_length=50, null=True, unique=True, blank=True)
    name = models.CharField(max_length=100, null=True, unique=True, blank=True)
    weight = models.FloatField()
    raza = models.ForeignKey(Raza, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birth_date = models.DateField()
    sex = models.CharField(max_length=10, choices=(('Male', 'Macho'), ('Female', 'Hembra')))
    purity_qualifier = models.ForeignKey(CalificadorPureza, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
    father = models.CharField(max_length=50, null=True, blank=True)
    mother = models.CharField(max_length=50, null=True, blank=True)
    
    establishment = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sheep')
    status = models.CharField(max_length=10, choices=[('active', 'Activa'), ('sold', 'Vendida'), ('dead', 'Muerta'),('stolen','Robada')], default='active')

    purchased = models.BooleanField(default=False)
    for_sale = models.BooleanField(default=False)

    individual_sale_value = models.FloatField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    origin_establishment = models.CharField(max_length=50, null=True, blank=True)
    
   

    def __str__(self):
        return self.name if self.name else self.RP
    
    def classify_age(self):
        if self.age <= 6:  # Lamb if 6 months or less
            return 'Lamb' if self.sex == 'Male' else 'Ewe Lamb'
        elif self.age <= 12:  # Yearling from 7 to 12 months
            return 'Yearling' if self.sex == 'Male' else 'Yearling Ewe'
        else:  # Adult sheep (older than 12 months)
            return 'Ram' if self.sex == 'Male' else 'Ewe'
        

# modelo para tabla de ventas

class Venta(models.Model):
    """
    Represents a sale of sheep.

    Attributes:
        id (int): The unique identifier for the sale.
        sheep (ManyToManyField): A list of sheep associated with the sale.
        sale_date (date): The date of the sale.
        total_weight (Decimal): The total weight of the sheep sold.
        meat_value (float): The value of the meat (relevant for sales to frigorificos).
        total_value (float): The total value of the sale.
        establishment (ForeignKey): The establishment making the sale (related to User).
        sale_type (str): The type of sale ('remate', 'individual', 'frigorifico', or 'donacion').
    """

    id = models.AutoField(primary_key=True)
    sheep = models.ManyToManyField('Oveja', related_name='sales', blank=True)  # For support of batch or individual sale
    sale_date = models.DateField()
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    meat_value = models.FloatField(null=True, blank=True)  # Only necessary for frigorífico
    total_value = models.FloatField(default=0.0)
    establishment = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sales')
    sale_type = models.CharField(max_length=20, choices=[('auction', 'Remate'), ('individual', 'Individual'), ('slaughterhouse', 'Frigorífico'), ('donation', 'Donación')])

    def __str__(self):
        sheep_names = ", ".join(sheep.name for sheep in self.sheep.all())
        return f"Sale on {self.sale_date} - Type: {self.sale_type} - Sheep: {sheep_names}"
    






   
    
    
   

    
    
    
    



   