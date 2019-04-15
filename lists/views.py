from django.shortcuts import render
# No londer need HttpResponse since we're handling HTTP with a template
from django.http import HttpResponse
from .models import Item


def home_page(request):
    if request.method == "POST":
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
    else:
        new_item_text = ''
    # Dj auto searches for the second argument inside any folders named
    # templates that are inside of one of your apps folders
    return render(request, 'home.html', {
        # use <dict>.get to supply a default value when POST is blank
        "new_item_text": new_item_text,
        })
