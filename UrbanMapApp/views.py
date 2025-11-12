from django.shortcuts import render
from django.conf import settings

def home(request):
    context = {
        'page_title': 'Χάρτης Αστικών Προβλημάτων',
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }
    return render(request, 'home.html', context)