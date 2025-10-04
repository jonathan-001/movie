from django.shortcuts import render, get_object_or_404
from .models import TVSeries, Season
from django.core.paginator import Paginator
from django.http import JsonResponse

def tvseries(request):
    # This view will power the main TV series listing page.
    series_list = TVSeries.objects.all().order_by('title')
    paginator = Paginator(series_list, 18) # Show 18 series per page

    page_number = request.GET.get('page')
    series_page = paginator.get_page(page_number)
    context = {
        'series_list': series_page
    }
    return render(request, 'tv-series.html', context)

def series_detail(request, series_id):
    series = get_object_or_404(TVSeries, pk=series_id)
    context = {
        'series': series
    }
    return render(request, 'series_detail.html', context)

def get_episodes_for_season(request, season_id):
    season = get_object_or_404(Season, pk=season_id)
    episodes = season.episodes.all().order_by('episode_number')
    episodes_data = list(episodes.values('id', 'title', 'episode_number'))
    return JsonResponse({'episodes': episodes_data})