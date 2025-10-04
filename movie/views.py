from django.shortcuts import render
from movies.models import Movie
from tvseries.models import TVSeries
from anime.models import Anime

def home(request):
    # Fetch the first 14 items for each category to display on the homepage
    # You can change the ordering later (e.g., by release date or rating)
    trending_movies = Movie.objects.all()[:14]
    latest_movies = Movie.objects.order_by('-id')[:14] # Assuming newer items have higher IDs
    latest_tvshows = TVSeries.objects.order_by('-id')[:14]
    anime_list = Anime.objects.all()[:14]

    context = {
        'trending_movies': trending_movies,
        'latest_movies': latest_movies,
        'latest_tvshows': latest_tvshows,
        'anime_list': anime_list,
    }
    return render(request, 'index.html', context)