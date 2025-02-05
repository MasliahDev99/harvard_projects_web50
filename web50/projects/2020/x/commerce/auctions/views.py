from django.contrib.auth import authenticate, login, logout
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

from .models import User
from .models import *

from . import utils 



def index(request):
    user = request.user
    watchlist_count = 0
    if user.is_authenticated:
        watchlist_count = len(utils.get_watchlist(user))
    
    auctions = utils.get_auctions_by(prefetch_watchlist=True,is_active=True)
    highest_bids = {
        auction.id: auction.bids.order_by('-amount').first() for auction in auctions
    }

    if request.method == 'POST':
        # Capture form values: auction ID and bid amount
        auction_id = request.POST.get('auction_id')
        bid_amount = request.POST.get('bid_amount')
        
        print(f"id: {auction_id} valor: {bid_amount}")
        # Retrieve the auction by ID
        auction = utils.get_auctions_by(id=auction_id).first()

        if auction:
            print(f"Nombre de subasta: {auction.title}")
            # Verify that the auction is active
            if auction.is_active:
                if utils.place_bid(auction, user, float(bid_amount)):
                    messages.success(request, 'Bid placed successfully.')
                    print(f"Se agrego con exito. ")
                else:
                    messages.error(request, 'Bid must be higher than the current highest bid.')
                    print(f"Entro al else")
            else:
                messages.error(request, 'Auction is not active or does not exist.')
                print(f"Entro al else final")
        else:
            messages.error(request, 'Auction not found.')
            print(f"Auction not found.")

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "highest_bids": highest_bids,
        "watchlist_count": watchlist_count,
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
            user = utils.create_user(username,email,password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
    

@csrf_protect
@login_required
def create(request):
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('starting_bid')
        category = request.POST.get('category')
        image_file = request.FILES.get('image')  # Changed from 'image_file' to 'image'
        user = request.user

        category_instance = utils.get_category_instance(category)

        if not category_instance:
            return render(request, 'auctions/create_listing.html', {
                "categories": categories,
                "error_message": "La categoría seleccionada no existe."
            })  

        end_date = request.POST.get('end_date')
        end_time = request.POST.get('end_time')

        new_auction = utils.create_auction(
            title=title,
            description=description,
            starting_bid=price,
            image=image_file,
            category=category_instance,
            created_by=user,
            end_date=end_date,
            end_time=end_time
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
        utils.delete_auction(auction_id=auction_id)
        return redirect('auction:index')
    
    return redirect('auctions:index')
    

@login_required
def wathclist_view(request):
    # obtenemos la lista de todas las subastas en la lista de seguimiento
    watchlists = utils.get_watchlist(request.user)
    return render(request,'auctions/watchlist.html',{
        "watchlists": watchlists,
    })
    

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
    return render(request,'auctions/categories.html',{
        "categories":categories,
    })


def category_auctions(request, category_name):
    # Buscar la categoría correspondiente en la base de datos
    category = Category.objects.filter(name=category_name).first()

    # Si la categoría existe, filtrar las subastas usando el método de utilidades
    if category:
        auctions = utils.get_auctions_by(category=category)
    else:
        auctions = []  # Si no existe la categoría, no hay subastas para mostrar

    return render(request, 'auctions/category_auctions.html', {
        "auctions": auctions,
        "category_name": category_name,  # Para mostrar el nombre de la categoría
    })


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
