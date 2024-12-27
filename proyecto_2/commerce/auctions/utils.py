from django.db import IntegrityError
from .models import User, Auction, Bid, Comment,Watchlist
from .models import Category as Categorie
# metodos de gestion de usuarios

def create_user(username, email, password):
    # Verifica si el usuario ya existe
    if exists_user(username):
        raise IntegrityError("Username already exists")
    
    user = User(username=username, email=email)
    user.set_password(password)  # Cifra la contraseña
    user.save()
    return user

# agregar datos opcionales, address y phone 
def add_user_data(user,address=None,phone=None):
    user.address = address
    user.phone = phone
    user.save()
    return True

# verifica si existe un usuario con el username
def exists_user(username):
    return User.objects.filter(username=username).exists()

# retorna el usuario por id o por username
def get_user_by(id=None,username=None):
    if id:
        return User.objects.get(id=id)
    if username:
        return User.objects.get(username=username)
    return None



# metodos de gestion de categorias
def create_category(name):
    category = Categorie(name=name)
    category.save()
    return category

def get_categories():
    return Categorie.objects.all()

def remove_categorie(name):
    category = Categorie.objects.get(name=name)
    category.delete()
    return True

# metodos de gestion de subastas
def create_auction(title,description,starting_bid,image_url,category,created_by):
    auction = Auction(title=title,description=description,starting_bid=starting_bid,image_url=image_url,category=category,created_by=created_by)
    auction.save()
    return auction

# obtener una subasta por parametros de busqueda
def get_auctions_by(**kwargs):
    return Auction.objects.filter(**kwargs)

# obtener todas las subastas
def get_all_auctions():
    return Auction.objects.all()

# metodos de gestion de ofertas
def create_bid(auction,user,amount):
    bid = Bid(auction=auction,user=user,amount=amount)
    bid.save()
    return bid

def place_bid(auction, user, amount):
    # Verificar si la subasta está activa
    if auction.is_active:
        # Obtener la última oferta (si existe)
        last_bid = auction.bids.order_by('-amount').first()

        # Si no hay oferta previa o si la nueva oferta es mayor que la anterior
        if not last_bid or last_bid.amount < amount:
            # Crear la nueva oferta
            bid = create_bid(auction, user, amount)
            return True
    # Si la subasta no está activa o la oferta no es mayor que la última
    return False
    


# metodos de gestion de comentarios



# metodos de gestion de listas de seguimiento




