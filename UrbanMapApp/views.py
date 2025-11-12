# UrbanMapApp/views.py

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Report, Category
from django.contrib.auth.decorators import login_required


def home(request):

    if request.method == 'POST' and request.user.is_authenticated:
        # Get data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        category_id = request.POST.get('category')
        photo = request.FILES.get('photo')
        category = Category.objects.get(id=category_id)



        if category and photo:
            new_report = Report(
                user=request.user,
                title=title,
                description=description,
                photo=photo,
                latitude=latitude,
                longitude=longitude,
                category=category
            )
            new_report.save()

        return redirect('home')
    else:
        categories = Category.objects.all()
        context = {
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'categories': categories,
        }
        return render(request, 'home.html', context)