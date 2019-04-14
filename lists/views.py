from django.shortcuts import render
# No londer need HttpResponse since we're handling HTTP with a template
from django.http import HttpResponse


def home_page(request):
    # Dj auto searches for the second argument inside any folders named
    # templates that are inside of one of your apps folders
    return render(request, 'home.html', {
        # use <dict>.get to supply a default value when POST is blank
        "new_item_text": request.POST.get('item_text', ''),
        })
