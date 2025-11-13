# UrbanMapApp/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings

from .models import Report, Category, Vote
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse


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
        pending_reports = Report.objects.exclude(status='RESOLVED')

        # --- Top 5 Reports Logic ---
        # 1. Calculate the score for each report
        # We create a list of tuples: (report_object, score)
        scored_reports = []
        for report in pending_reports:
            score = report.calculate_priority_score()
            scored_reports.append((report, score))

        # 2. Sort the list in descending order based on the score
        # The key=lambda item: item[1] tells sort to use the second element (the score)
        scored_reports.sort(key=lambda item: item[1], reverse=True)

        # 3. Get just the top 5 report objects from the sorted list
        top_5_reports = [item[0] for item in scored_reports[:5]]
        reports_data = []
        for report in reports:
            category_name = report.category.name if report.category else "No Category"

            photo_url = report.photo.url if report.photo else ""

            reports_data.append({
                'id': report.id,
                'lat': float(report.latitude),
                'lng': float(report.longitude),
                'title': report.title,
                'description': report.description,
                'category': category_name,
                'photo_url': photo_url,
                'status': report.status,
                'vote_count': report.votes.count(),
            })

        reports_json = json.dumps(reports_data)

        context = {
            'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
            'categories': categories,
            'reports_json': reports_json,
            'top_5_reports': top_5_reports,
        }
        return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def upvote_report(request, report_id):
    if request.method == 'POST':
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Report not found.'}, status=404)

        #user already voted.
        vote, created = Vote.objects.get_or_create(user=request.user, report=report)
        if not created:
            # If the vote already existed (was not created), delete it.
            vote.delete()
            action = 'unvoted'
        else:
            # If the vote was just created.
            action = 'voted'
        vote_count = report.votes.count()

        # 'created' is True if a new vote was made, False if it already existed.
        return JsonResponse({
            'success': True,
            'vote_count': vote_count,
            'action': action
        })

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)