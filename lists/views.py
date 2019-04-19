from django.shortcuts import render, redirect
# No londer need HttpResponse since we're handling HTTP with a template
from django.http import HttpResponse
from .models import Item


def home_page(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'])
        return redirect("/")

    items = Item.objects.all()
    # Dj auto searches for the second argument inside any folders named
    # templates that are inside of one of your apps folders
    return render(request, 'home.html', {'items': items})
