from django.shortcuts import render, redirect
from django.conf import settings
from .models import Report, Category
from django.contrib.auth.decorators import login_required

def home(request):


    if request.method == "POST":
        title = request.POST.get('title')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if request.user.is_authenticated:
            new_report = Report(
                user=request.user,
                title=title,
                description="default description",
                photo='report_photos/default.jpg',
                latitude=latitude,
                longitude=longitude,
            )
            new_report.save()
        return redirect("home")
    else:
        context = {
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        }
    return render(request, 'home.html', context)