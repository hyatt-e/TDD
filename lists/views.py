from django.shortcuts import render, redirect
# No londer need HttpResponse since we're handling HTTP with a template
from django.http import HttpResponse
from .models import Item, List


def home_page(request):
    # Dj auto searches for the second argument inside any folders named
    # templates that are inside of one of your apps folders
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')
