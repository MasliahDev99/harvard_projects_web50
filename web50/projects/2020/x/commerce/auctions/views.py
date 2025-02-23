from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from datetime import datetime
from django.utils import timezone
import pytz
from .models import User
from .models import *

from . import utils 



#home
def home(request):
    categories = utils.get_categories()
    return render(request,'auctions/home.html',{
        "categories":categories,
    })


# active listings

def index(request):
    user = request.user
    watchlist_count = 0
    auctions = []
    auctions_watchlisted = []
    paginator = Paginator(auctions, 10) # show 10 auctions per page

    page = request.POST.get('page')

    if user.is_authenticated:
        watchlist_count = len(utils.get_watchlist(user))
        auctions_watchlisted = utils.get_user_watchlist_auctions(user, is_active=True)

    auctions = utils.get_auctions_by(is_active=True)
    highest_bids = {
        auction.id: auction.bids.order_by('-amount').first() for auction in auctions
    }

    if request.method == 'POST':
       utils.handle_bid_post_request(request,user)


    desired_timezone = 'America/Montevideo'
    current_time = timezone.localtime(timezone.now(), timezone=pytz.timezone(desired_timezone))
    print(f"Current time: {current_time}\n")

    # check if auction is ended
    utils.check_and_close_ended_auctions(current_time)

    # Update auctions list after checking for ended ones
    auctions = utils.get_auctions_by(is_active=True)

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "highest_bids": highest_bids,
        "watchlist_count": watchlist_count,
        "auctions_watchlisted": auctions_watchlisted,
        "current_time": current_time,
    })



@login_required
def bid_history(request):
    user_bids = Bid.objects.filter(user=request.user).select_related('auction')

    for bid in user_bids:
        highest_bid = bid.auction.bids.order_by('-amount').first()
        if not bid.auction.is_finished:
            bid.status = 'In Process'
        else:
            if highest_bid == bid:
                bid.status = 'Winner'
            else:
                bid.status = 'Lost'

    return render(request,'auctions/auction_history.html',{
        "user_bids": user_bids,
    })

@login_required
def closed_listings(request):
    auctions = utils.get_auctions_by(is_active=False)
    highest_bids = {
        auction.id: auction.bids.order_by('-amount').first() for auction in auctions
    }
    return render(request,'auctions/closed_listings.html',{
        "auctions": auctions,
        "highest_bids": highest_bids,
    })



#funciona
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect('auctions:index')
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request,'auctions/login.html')


#funciona
@login_required
def logout_view(request):
    logout(request)
    return redirect('auctions:index')


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = utils.create_user(username, email, password)
            if user is None:
                raise ValueError("User creation failed.")
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        except ValueError as e:
            return render(request, "auctions/register.html", {
                "message": str(e)
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    

@csrf_protect
@login_required
def create(request):
    categories = utils.get_categories()

    if request.method == "POST":
        new_auction_data = utils.handle_create_post_request(request)

        category_instance = utils.get_category_instance(new_auction_data['category'])

        if not category_instance:
            return render(request, 'auctions/create_listing.html', {
                "categories": categories,
                "error_message": "Category not exists."
            })

        # Crear la subasta
        new_auction = utils.create_auction(
            title=new_auction_data['title'],
            description=new_auction_data['description'],
            starting_bid=new_auction_data['price'],
            image=new_auction_data['image_file'],
            category=category_instance,
            created_by=new_auction_data['user'],
            end_date=new_auction_data['end_date'],
            end_time=new_auction_data['end_time']
        )

        return redirect('auctions:index')
    else:
        return render(request, 'auctions/create_listing.html', {
            "categories": categories,
        })


@csrf_protect
@login_required
def delete_auction(request,auction_id):
    # obtenemos la subasta por id
    auction = utils.get_auctions_by(id=auction_id).first()
    # si la subasta existe y si es el usuario creador
    if auction and auction.created_by == request.user:
        utils.close_auction(auction_id)
        return redirect('auctions:index')
    
    return redirect(request.META.get('HTTP_REFERER', 'auctions:index'))
    

@login_required
def wathclist_view(request):
    # obtenemos la lista de todas las subastas en la lista de seguimiento
    watchlists = utils.get_watchlist(request.user)
    return render(request,'auctions/watchlist.html',{
        "watchlists": watchlists,
    })
    

#refactorizar
@login_required    
def add_to_watchlist(request, auction_id):
    # si el usuario no esta authenticado redirigimos al login
    if not request.user.is_authenticated:
        return redirect('auctions:login')

    # Obtén la subasta o lanza un error 404 si no existe
    auction = utils.get_auctions_by(id=auction_id).first()

    if not auction:
        return redirect('auctions:index')  # Redirigir si no se encuentra la subasta

    # Usuario autenticado
    user = request.user

    # Verifica si la subasta ya está en la lista de seguimiento
    auction_watchlist = utils.search_auctions_in_watchlist(user, auction)

    if auction_watchlist:
        # si ya esta en la subasta eliminamos
        utils.remove_from_watchlist(auction,user)
        # cambiamos el esatdo de is_watchlist a False
        auction.is_watchlist = False
    else:
        # si no esta en la lista de seguimiento la agregamos
        utils.add_to_watchlist(auction,user)
        # cambiamos el esatdo de is_watchlist a True
        auction.is_watchlist = True

    auction.save()

    # Redirige a la página desde donde se hizo la acción
    return redirect(request.META.get('HTTP_REFERER', 'auctions:index'))


def categories(request):
    categories = utils.get_categories()
    categories_with_active_counts = [
        {
            "name": category.name,
            "active_count": utils.active_auctions_count_by_category(category),
        } for category in categories
    ]
    return render(request,'auctions/categories.html',{
        "categories":categories_with_active_counts,
    })


def category_auctions(request, category_name):
    # Buscar la categoría correspondiente en la base de datos
    category = Category.objects.filter(name=category_name).first()

    # Si la categoría existe, filtrar las subastas usando el método de utilidades
    if category:
        auctions = utils.get_auctions_by(category=category,prefetch_watchlist=True,is_active=True)
      
    else:
        auctions = []  # Si no existe la categoría, no hay subastas para mostrar

    return render(request, 'auctions/category_auctions.html', {
        "auctions": auctions,
        "category_name": category_name,  # Para mostrar el nombre de la categoría
        
    })

@login_required
def comments(request,auction_id):
    auction = utils.get_auctions_by(id=auction_id).first()

    if not auction:
        return redirect('auctions:index')

    if request.method == 'POST':
        content = request.POST.get('comment')
        if content:
            utils.create_comment(auction,request.user,content)
            messages.success(request,'Comment added successfully.')
        else:
            messages.error(request,'Comment cannot be empty.')
        
        return redirect('auctions:auction_comments',auction_id=auction_id)
    
    
    
    comments = utils.get_comments_for_auction(auction)
    return render(request,'auctions/comments_auction.html',{
        "auction":auction,
        "comments":comments,
    })

@login_required
def comment_reply(request, auction_id, comment_id):
    if request.method == 'POST':
        parent_comment = get_object_or_404(Comment, id=comment_id)
        content = request.POST.get('reply')
        if content:
            utils.create_reply(parent_comment, request.user, content)
            messages.success(request, 'Reply added successfully.')
        else:
            messages.error(request, 'Reply cannot be empty.')
        return redirect('auctions:auction_comments', auction_id=auction_id)

@csrf_protect
@login_required
def delete_comment(request, auction_id,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)

    if request.user == comment.user:
        utils.delete_comment(comment_id)
        messages.success(request,f'Comment deleted successfully.')
    else:
        messages.error(request,'You do not have permission to delete this comment.')
    return redirect('auctions:auction_comments',auction_id=auction_id)


@csrf_protect
@login_required
def update_comment(request,auction_id,comment_id):
    comment = get_object_or_404(Comment,id=comment_id)

    if request.method == 'POST':
        new_content = request.POST.get('new_content')
        if new_content:
            utils.update_comment(comment_id,new_content)
            messages.success(request,'Comment updated successfully.')
        else:
            messages.error(request,'Comment cannot be empty.')
        return redirect('auctions:auction_comments',auction_id=auction_id)



@csrf_protect
@login_required
def place_bid(request, auction_id):
    if request.method == 'POST':
        auction = get_object_or_404(Auction, id=auction_id)
        bid_amount = float(request.POST.get('bid_amount', 0))

  
        highest_bid = auction.bids.order_by('-amount').first()
        current_price = highest_bid.amount if highest_bid else auction.starting_bid

        if bid_amount and float(bid_amount) > current_price:
            success = utils.create_bid(auction, request.user, bid_amount)
            if success:
                messages.success(request, 'Bid placed successfully.')
            else:
                messages.error(request, 'Bid amount must be higher than the current price.')
        else:
            messages.error(request, 'Invalid bid amount.')
    
    return redirect('auctions:listing_detail', auction_id=auction_id)


def listing_detail(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, 'auctions/components/listing_detail.html',{'auction':auction})

