from django.db import IntegrityError
from .models import User, Auction, Bid, Comment,Watchlist
from .models import Category as Categorie
from django.contrib import messages
from datetime import datetime
from django.db.models import Prefetch
from django.utils import timezone
import pytz

"""

    Porpuse of utils method

    create_user: crea un usuario






"""








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


def get_category_instance(category_name):
    try:
        category = Categorie.objects.get(name=category_name)
        return category
    except Categorie.DoesNotExist:
        return None

# metodos de gestion de subastas
def create_auction(title, description, starting_bid, image, category, created_by, end_date, end_time):
   
    auction = Auction(
        title=title,
        description=description,
        starting_bid=starting_bid,
        image = image,
        category=category,
        created_by=created_by,
        end_date=end_date,
        end_time=end_time
    )
    
    auction.save()
    return auction

def delete_auction(auction_id):

    try:
        auction = Auction.objects.get(id=auction_id)
        auction.delete()
    except Auction.DoesNotExist:
        return False

    return True


def get_user_watchlist_auctions(user,**kwargs):
    """
        Obtiene las subastas que estan en la lista de seguimiento del usuario.
    """
    return Auction.objects.filter(
        watchlisted_by__user = user,
        **kwargs
    ).prefetch_related(
        Prefetch('watchlisted_by', queryset=Watchlist.objects.filter(user=user),to_attr='user_watchlist')
    )



# obtener una subasta por parametros de busqueda ( este metodo es mas flexible) 
def get_auctions_by(request=None,prefetch_watchlist=False, **kwargs):
    queryset = Auction.objects.filter(**kwargs)


    # Si se requiere, prefetch los elementos relacionados
    if prefetch_watchlist:
        queryset = queryset.prefetch_related(
            #obtenemos todas las subastas que pertenecen a la lista de seguimiento del usuario
            Prefetch('watchlisted_by', queryset=Watchlist.objects.all(), to_attr='user_watchlist')
        )
    
    return queryset

# obtener todas las subastas
def get_all_auctions(prefetch_watchlist=False):
    queryset = Auction.objects.all()
    if prefetch_watchlist:
        queryset = queryset.prefetch_related(
            Prefetch('watchlisted_by', queryset=Watchlist.objects.all(), to_attr='user_watchlist')
        )
    return queryset

# metodos de gestion de ofertas
def create_bid(auction,user,amount):
    bid = Bid(auction=auction,user=user,amount=amount)
    bid.save()
    return bid

def place_bid(auction, user, amount):
    # Verificamos si la subasta está activa
    print(f"Subasta activa: {auction.is_active}")
    if auction.is_active:
        # Obtenemos la ultima oferta (si existe)
        last_bid = auction.bids.order_by('-amount').first()
        print(f"Ultima oferta: {last_bid}""")
        # Obtenemos la oferta inicial
        minimum_bid = auction.starting_bid
        print(f"Oferta inicial: {minimum_bid}")

        # Si no hay oferta previa, la oferta debe ser mayor que la oferta inicial
        if not last_bid and amount > minimum_bid:
            # Creamos la nueva oferta
            bid = create_bid(auction, user, amount)
            return True
        # Si hay oferta previa, la nueva oferta debe ser mayor que la última
        elif last_bid and last_bid.amount < amount:
            # Creamos la nueva oferta
            bid = create_bid(auction, user, amount)
            return True
    # Si la subasta no está activa o la oferta no es válida
    return False


def close_auction(auction_id):
    try:
        auction = Auction.objects.get(id=auction_id)
        auction.is_active = False
        auction.save()
        return True
    except Auction.DoesNotExist:
        return False


def active_auctions_count_by_category(category):
    return Auction.objects.filter(category=category,is_active=True).count()

    


# metodos de gestion de comentarios



# metodos de gestion de listas de seguimiento




def add_to_watchlist(auction,user):
    watchlist = Watchlist(auction=auction,user=user)
    watchlist.save()
    return watchlist
    
def remove_from_watchlist(auction,user):
    watchlist = Watchlist.objects.get(auction=auction,user=user)
    watchlist.delete()
    return True


def search_auctions_in_watchlist(user, auction):
    return Watchlist.objects.filter(user=user, auction=auction).first()

def get_watchlist(user):
    return Watchlist.objects.filter(user=user)



def create_reply(parent_comment,user,content):
    reply = Comment(auction=parent_comment.auction,parent=parent_comment,user=user,content=content)
    reply.save()
    return reply

def create_comment(auction,user,content):
    comment = Comment(auction=auction,user=user,content=content)
    comment.save()
    return comment

def get_comments_for_auction(auction):
    return Comment.objects.filter(auction=auction)

def delete_comment(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return True
    except Comment.DoesNotExist:
        return False

def update_comment(comment_id,new_content):
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.content = new_content
        comment.save()
        return True
    except Comment.DoesNotExist:
        return False







# 
# determinamos el ganador de una subasta
def determine_auction_winner_and_close(auction):
    highest_bid = auction.bids.order_by('-amount').first()
    if highest_bid:
        auction.winner = highest_bid.user  
        auction.is_finished = True    
    else:
        auction.is_active = False

    auction.save()

def determine_auction_winners():
    ended_auctions = Auction.objects.filter(end_date__lte=timezone.now(), winner__isnull=True)
    for auction in ended_auctions:
        determine_auction_winner_and_close(auction)
    
    

def get_current_time_in_timezone(timezone_name):
    try:
        desired_timezone = pytz.timezone(timezone_name)
        current_time = timezone.localtime(timezone.now(),desired_timezone)
    except Exception as e:
        current_time = None
    return current_time


def check_and_close_ended_auctions(current_time):
    ended_auctions = get_auctions_by(is_active=True)
    for auction in ended_auctions:
        auction_end = timezone.make_aware(datetime.combine(auction.end_date, auction.end_time))
        auction_end = timezone.localtime(auction_end, timezone=pytz.timezone('America/New_York'))
        print(f"auction_end: {auction_end} - Current time: {current_time}\n")

        if auction_end <= current_time:
            determine_auction_winner_and_close(auction)
            print(f"Auction {auction.title} has ended.")

    return ended_auctions


def handle_bid_post_request(request,user):
   
    auction_id = request.POST.get('auction_id')
    bid_amount = request.POST.get('bid_amount')
    
    auction = get_auctions_by(id=auction_id).first()
    
    if auction:
        if auction.is_active:
            if place_bid(auction, user, float(bid_amount)):
                messages.success(request, 'Bid placed successfully.')
            else:
                messages.error(request, 'Bid must be higher than the current highest bid.')
        else:
            messages.error(request, 'Auction is not active or does not exist.')
    else:
        messages.error(request, 'Auction not found.')





def handle_create_post_request(request):
    return {
        'title': request.POST.get('title'),
        'description': request.POST.get('description'),
        'price': request.POST.get('starting_bid'),
        'category': request.POST.get('category'),
        'image_file': request.FILES.get('image'),  # Changed from 'image_file' to 'image'
        'end_date': request.POST.get('end_date'),
        'end_time': request.POST.get('end_time'),
        'user': request.user,
    }







    








