from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from . import util

import json
import markdown2
from markdown2 import Markdown
import random

#finished
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


#finished
def entry(request,title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "Entry not found."
        })
    return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": markdown2.markdown(content)
        })

   
def search(request):
    """
        si la consulta coincide con el nombre de una entrada de enciclopedia, 
        el usuario debe ser redirigido a la página de esa entrada.
        Si la consulta no coincide con el nombre de una entrada de enciclopedia, 
        el usuario debería ser redirigido a una página de resultados de búsqueda 
        que muestra una lista de todas las entradas de enciclopedia que tienen la consulta 
        como subcadena. Por ejemplo, si la consulta de búsqueda fuera ytho, 
        entonces Pythondebería aparecer en los resultados de búsqueda.
        Al hacer clic en cualquiera de los nombres de entrada en 
        la página de resultados de búsqueda, 
        el usuario debería ir a la página de esa entrada.
    """
    query = request.POST.get('q','')
    if util.get_entry(query):
        return redirect('encyclopedia:entry', title=query)
    else:

        entries = util.list_entries()
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request,'encyclopedia/results.html',{
            "results": results
        })
    

#finished    
def new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        #if the new title exists give a error message
        if util.get_entry(title):
            return render(request,"encyclopedia/new_entry.html",{
                "error_message": f"The title '{title}' exists. Please put other title."
            })

        markdown = Markdown()
        try:

            html_content = markdown.convert(content)
            
        except Exception as e:
             return render(request, "encyclopedia/new_entry.html", {
                "error_message": "Invalid Markdown format. Please check your content."
            })
        #save the new entrie and redirect to the new entrie page
        util.save_entry(title=title,content=content)
        
        return redirect('encyclopedia:entry',title=title)
    
    #si es el method es GET
    return render(request, 'encyclopedia/new_entry.html')


def edit_page(request):
    
    return redirect('index')
def random_page(request):
    entries = util.list_entries()
    random_page = random.choice(entries)
    print(f"pagina random: {random_page}")
    return redirect('encyclopedia:entry',title=random_page)