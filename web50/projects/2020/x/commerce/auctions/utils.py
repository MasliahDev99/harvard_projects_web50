from django.db import IntegrityError
from .models import User, Auction, Bid, Comment,Watchlist
from .models import Category as Categorie
from django.contrib import messages
from datetime import datetime
from django.db.models import Prefetch
from django.utils import timezone
import pytz

"""
    Utils methods for auctions app
"""


# User managment methods

def create_user(username, email, password):
    """
        Create a new user

        args:
            username: username of the user
            email: email of the user
            password: password of the user
        return:
            user: user object
        except:
            IntegrityError: if the user is not valid
    """
    try:
        # Verifica si el usuario ya existe
        if exists_user(username):
            raise IntegrityError("Username already exists")
        
        user = User(username=username, email=email)
        user.set_password(password)  # Cifra la contraseña
        user.save()
        return user
    except IntegrityError as e:
        print(f"Integrity error creating user: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None


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



# Category managment methods
def create_category(name):
    """
        Create a new category

        args:
            name: name of the category
        return:
            category: category object
        except:
            IntegrityError: if the category is not valid

    """
    try:
        category = Categorie(name=name)
        category.save()
        return category
    except IntegrityError as e:
        print(f"Integrity error creating category: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None

def get_categories():
    return Categorie.objects.all()



def get_category_instance(category_name):
    """
        Get the category instance by name

        args:
            category_name: name of the category
        return:
            category: category object
        except:
            None: if the category does not exist
    """
    try:
        category = Categorie.objects.get(name=category_name)
        return category
    except Categorie.DoesNotExist:
        return None




# Auction managment methods
def create_auction(title, description, starting_bid, image, category, created_by, end_date, end_time):
    """
        Create a new auction

        args:
            title: title of the auction
            description: description of the auction
            starting_bid: starting bid of the auction
            image: image of the auction
            category: category of the auction
            created_by: user who created the auction
            end_date: date when the auction ends
            end_time: time when the auction ends
        return:
            auction: auction object
        excepts:
            IntegrityError: if the auction is not valid
    """
    try:
        auction = Auction(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image=image,
            category=category,
            created_by=created_by,
            end_date=end_date,
            end_time=end_time
        )
        
        auction.save()
        return auction
    except IntegrityError as e:
        print(f"Integrity error creating auction: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def delete_auction(auction_id):
    """
        Delete an auction
        args:
            auction_id: id of the auction
        return:
            True: if the auction was deleted
            False: if the auction does not exist
    """
    try:
        auction = Auction.objects.get(id=auction_id)
        auction.delete()
    except Auction.DoesNotExist:
        return False

    return True

def close_auction(auction_id):
    """
        Close an auction
        args:
            auction_id: id of the auction
        return:
            True: if the auction was closed
            False: if the auction does not exist
    """
    try:
        auction = Auction.objects.get(id=auction_id)
        auction.is_active = False
        auction.save()
        return True
    except Auction.DoesNotExist:
        return False

def get_user_watchlist_auctions(user,**kwargs):
    """
        Get the watchlist auction of a user
        args:
            user: user object
            **kwargs: filter params
        return:
            queryset: queryset of auctions
    """
    return Auction.objects.filter(
        watchlisted_by__user = user,
        **kwargs
    ).prefetch_related(
        Prefetch('watchlisted_by', queryset=Watchlist.objects.filter(user=user),to_attr='user_watchlist')
    )



# Get auctions methods  
def get_auctions_by(request=None,prefetch_watchlist=False, **kwargs):
    """
        Get auctions filter by params

        args:
            request: request object
            prefetch_watchlist: bool, if True, prefetch the watchlist of the user
            **kwargs: filter params
        return:
            queryset: queryset of auctions

    """
    queryset = Auction.objects.filter(**kwargs).order_by('-created_at')


    # Si se requiere, prefetch los elementos relacionados
    if prefetch_watchlist:
        queryset = queryset.prefetch_related(
            #obtenemos todas las subastas que pertenecen a la lista de seguimiento del usuario
            Prefetch('watchlisted_by', queryset=Watchlist.objects.all(), to_attr='user_watchlist')
        )
    return queryset


# Bid managment methods
def create_bid(auction,user,amount):
    """
        Creat a new bid for an auction

        args:
            auction: auction object
            user: user object
            amount: amount of the bid
        return:
            bid: bid object
        excepts:
            IntegrityError: if the bid is not valid

    """
    try:
        bid = Bid(auction=auction,user=user,amount=amount)
        bid.save()
        return bid
    except IntegrityError as e:
        print(f"Integrity error creating bid: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None

def place_bid(auction, user, amount):
    """
        Place a bid for an auction

        args:
            auction: auction object
            user: user object
            amount: amount of the bid
        return:
            bid: bid object

    """
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





def active_auctions_count_by_category(category):
    """
        Return the number of active auctions for a given category.
    """
    return Auction.objects.filter(category=category,is_active=True).count()

    


# Comments managment methods

def create_reply(parent_comment,user,content):
    """
        Creat a new reply for a comment

        args:
            parent_comment:  comment object
            user: user object
            content: content of the reply
        return:
            reply: comment object
        excepts:
            IntegrityError: if the comment is not valid
    """
    try:
        reply = Comment(auction=parent_comment.auction,parent=parent_comment,user=user,content=content)
        reply.save()
        return reply
    except IntegrityError as e:
        print(f"Error creating reply: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None

def create_comment(auction,user,content):
    """
        Create a new comment
        args:
            auction: auction object
            user: user object
            content: content of the comment
        return:
            comment: comment object
        except:
            IntegrityError: if the comment is not valid
    """
    try:
        comment = Comment(auction=auction,user=user,content=content)
        comment.save()
        return comment
    except IntegrityError as e:
        print(f"Error creating comment: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None

def get_comments_for_auction(auction):
    return Comment.objects.filter(auction=auction)

def delete_comment(comment_id):
    """ 
        Delete a comment and all its children comments recursively.    
        args:
            comment_id: id of the comment
        return:
            True: if the comment was deleted
            False: if the comment does not exist
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        # To resolve we need to chek if comment has children, using recursive functions
        def delete_with_children(comment):
            child_comments = Comment.objects.filter(parent=comment)
            for child in child_comments:
                delete_with_children(child) # Recursively delete child comments
            comment.delete() # here delete the comment itself

        delete_with_children(comment)
        return True
    
    except Comment.DoesNotExist:
        return False

def update_comment(comment_id,new_content):
    """
        Update a comment
        args:
            comment_id: id of the comment
            new_content: new content of the comment
        return:
            True: if the comment was updated
            False: if the comment does not exist
    """
    try:
        comment = Comment.objects.get(id=comment_id)
        comment.content = new_content
        comment.save()
        return True
    except Comment.DoesNotExist:
        return False



# Watchlist managment methods




def add_to_watchlist(auction,user):
    """
        Add an auction to the watchlist
        args:
            auction: auction object
            user: user object
        return:
            watchlist: watchlist object
    """
    try:
        watchlist = Watchlist(auction=auction,user=user)
        watchlist.save()
        return watchlist
    except IntegrityError as e:
        print(f"Error adding to watchlist: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None
    
def remove_from_watchlist(auction,user):
    """
        Remove an auction from the watchlist
        args:
            auction: auction object
            user: user object
        return:
            True: if the auction was removed
            False: if the auction does not exist
    """
    try:
        watchlist = Watchlist.objects.get(auction=auction,user=user)
        watchlist.delete()
        return True
    except IntegrityError as e:
        print(f"Error adding to watchlist: {e}")
        return None
    except Exception as e:
        print(f"An error ocurred: {e}")
        return None


def search_auctions_in_watchlist(user, auction):
    """
        Search an auction in the watchlist
        args:
            user: user object
            auction: auction object
        return:
            watchlist: watchlist object
    """
    return Watchlist.objects.filter(user=user, auction=auction).first()

def get_watchlist(user):
    """
        Get the watchlist of a user
        args:
            user: user object
        return:
            watchlist: watchlist object
    """
    return Watchlist.objects.filter(user=user)











# determinados el ganador de una subasta
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
        'image_file': request.FILES.get('image'),  
        'end_date': request.POST.get('end_date'),
        'end_time': request.POST.get('end_time'),
        'user': request.user,
    }







    








