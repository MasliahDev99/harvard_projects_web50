from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Modelo de usuario personalizado
class User(AbstractUser):
    address = models.CharField(max_length=100, blank=True, null=True)  
    phone = models.CharField(max_length=10, blank=True, null=True)  

    def __str__(self):
        return self.username

# Categoría para las subastas
class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# Modelo para una subasta
class Auction(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)

    image = models.ImageField(upload_to='images/auctions/',blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="auctions")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="auctions")
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=True)
    is_finished = models.BooleanField(default=False)

    is_watchlisted = models.BooleanField(default=False)

    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_auctions')

    # fecha de finalizacion  y hora de finalizacion
    end_date = models.DateField(default='2023-12-31')
    end_time = models.TimeField(default='00:00:00')

    def __str__(self):
        return self.title

# Modelo para las pujas
class Bid(models.Model):
    id = models.BigAutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('winner', 'Winner'),
        ('lost', 'Lost'),
        ('in_process', 'In Process'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='in_process',
    )


    def __str__(self):
        return f"{self.user.username} - ${self.amount}"

# Modelo para los comentarios
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    #para subcomentarrios
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.user.username} en {self.auction.title}"

# Modelo para la lista de seguimiento (Watchlist)
class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)
    #cantidad de subastas en la lista de seguimiento
  
    
  

    def __str__(self):
        return f"{self.user.username} - {self.auction.title}"