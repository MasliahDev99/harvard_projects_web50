from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import User
from .models import *

# Create your views here.

def index(request):
    return render(request, 'ganaderia/index.html')





def register_view(request):
    return render(request, 'ganaderia/register.html')

def login_view(request):
    return render(request, 'ganaderia/login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request,'ganaderia/index.html')

@login_required
def dashboard(request):
    return render(request, 'ganaderia/dashboard.html')

@login_required
def ventas(request):
    return render(request, 'ganaderia/ventas.html')

@login_required
def ovejas(request):
    return render(request, 'ganaderia/ovejas.html')

@login_required
def planteletas(request):
    return render(request, 'ganaderia/planteletas.html')