from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings

# Create your views here.
def movies(request):
    movie_list = Movie.objects.all().order_by('title') # Order for consistent pagination
    paginator = Paginator(movie_list, 18) # Show 18 movies per page

    page_number = request.GET.get('page')
    movies_page = paginator.get_page(page_number)
    context = {
        'movies': movies_page
    }
    return render(request, 'movies.html', context)

def search_view(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Using Q objects for a more complex query if needed in the future
        # Here we search in the title field, case-insensitively.
        results = Movie.objects.filter(Q(title__icontains=query)).order_by('title')

    context = {
        'query': query,
        'results': results,
        'results_count': results.count() if results else 0,
    }
    return render(request, 'search_results.html', context)

import requests

def movie_detail_view(request, imdb_id):
    # First, get the local movie object to access local data like watch/download links
    local_movie = get_object_or_404(Movie, imdb_id=imdb_id)

    # Construct the API URL using the key from settings
    api_url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={settings.OMDB_API_KEY}'
    context = {'local_movie': local_movie} # Start context with local data

    try:
        response = requests.get(api_url)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        movie_data = response.json()

        if movie_data.get('Response') == 'True':
            # If API call is successful, add API data to the context
            context['api'] = movie_data

            # Save the poster URL from the API to our local movie object
            poster_url = movie_data.get('Poster')
            if poster_url and poster_url != 'N/A' and local_movie.poster_api_url != poster_url:
                local_movie.poster_api_url = poster_url
                local_movie.save(update_fields=['poster_api_url'])

        else:
            # API returned an error (e.g., "Movie not found")
            context['api_error'] = movie_data.get('Error', 'Unknown API error')

    except requests.exceptions.RequestException as e:
        # Handle network or API error
        context['api_error'] = f'Could not connect to the movie database: {e}'
    
    # Render the main detail page. The template will decide what to show
    # based on whether 'api' or 'api_error' is in the context.
    return render(request, 'movie_detail.html', context)
