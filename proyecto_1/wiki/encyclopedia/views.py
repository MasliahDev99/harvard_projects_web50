from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.http import Http404
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

#finished
def search(request):

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
        try:
            new_title = save_or_edit(request)
        except ValueError as e:
             return render(request, "encyclopedia/new_entry.html", {
                "error_message": str(e)
            })
        return redirect('encyclopedia:entry',title=new_title)
    
    #si es el method es GET
    return render(request, 'encyclopedia/new_entry.html')

#finished
def edit_page(request, title):
    content = util.get_entry(title)
    if request.method == 'POST':
        title2 = request.POST.get('title') 
        try:
            
            if title2!= title:
                util.delete_entry(title)

            new_title = save_or_edit(request, title=title)
            return redirect('encyclopedia:entry', title=new_title)
        except ValueError as e:
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "content": content,
                "error_message": str(e)
            })

    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "content": content
    })


def save_or_edit(request,title=None):
    new_title = request.POST.get('title',title)
    new_content = request.POST.get('content')
    
    if not new_title and not new_content:
        raise ValueError("Title and content cannot be empty.")
    
    if title is None and util.get_entry(new_title):
        raise ValueError(f"The title '{new_title}' already exists, please put other title.")
    
    util.validate_markdown(new_content)
    util.save_entry(new_title,new_content)
    
    return new_title

#finished
def random_page(request):
    entries = util.list_entries()
    random_page = random.choice(entries)
    print(f"pagina random: {random_page}")
    return redirect('encyclopedia:entry',title=random_page)




