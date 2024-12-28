from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import User
from .models import *

from . import utils 



def index(request):
    user = request.user
    watchlist_count = 0
    if user.is_authenticated:
        watchlist_count = len(utils.get_watchlist(user))
    return render(request, "auctions/index.html", {
        "auctions": utils.get_all_auctions(),
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
    

@login_required
def create(request):
    # obtenemos todas las categorias para una subasta
    categories = Category.objects.all()

    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('starting_bid')
        category = request.POST.get('category')
        image = request.FILES.get('image_url')
        user = request.user

        # creamos la subasta y la guardamos
        new_auction = utils.create_auction(title,description,price,category,image,user)
        return redirect('auctions:index')
    else:
        return render(request,'auctions/create_listing.html',{
            "categories":categories,
        })
    


def wathclist_view(request):
    # obtenemos la lista de todas las subastas en la lista de seguimiento
    watchlists = utils.get_watchlist(request.user)
    return render(request,'auctions/watchlist.html',{
        "watchlists": watchlists,
    })
    

    
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
        # Puedes redirigir de nuevo o retornar algún mensaje si lo deseas
        return redirect(request.META.get('HTTP_REFERER', 'auctions:index'))
    
    utils.add_to_watchlist(auction,user)

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