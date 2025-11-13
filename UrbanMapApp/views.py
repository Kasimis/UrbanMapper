# UrbanMapApp/views.py

from django.shortcuts import render, redirect
from django.conf import settings
from .models import Report, Category
import json


def home(request):
    if request.method == 'POST' and request.user.is_authenticated:
        title = request.POST.get('title')
        description = request.POST.get('description')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        category_id = request.POST.get('category')
        photo = request.FILES.get('photo')

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None

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
        reports = Report.objects.all()

        reports_data = []
        for report in reports:
            category_name = report.category.name if report.category else "No Category"

            photo_url = report.photo.url if report.photo else ""

            reports_data.append({
                'lat': float(report.latitude),
                'lng': float(report.longitude),
                'title': report.title,
                'description': report.description,
                'category': category_name,
                'photo_url': photo_url
            })

        reports_json = json.dumps(reports_data)

        context = {
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'categories': categories,
            'reports_json': reports_json,
        }
        return render(request, 'home.html', context)