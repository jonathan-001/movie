from django.shortcuts import render, get_object_or_404
from .models import Anime
from django.core.paginator import Paginator

# Create your views here.
# anime/views.py
from jikanpy import Jikan # Import the Jikan Python wrapper

def anime(request):
    anime_list = Anime.objects.all().order_by('title')
    paginator = Paginator(anime_list, 18) # Show 18 anime per page

    page_number = request.GET.get('page')
    anime_page = paginator.get_page(page_number)
    context = {
        'anime_list': anime_page
    }
    return render(request, 'anime.html', context)

def top_airing_anime(request):
    """
    Fetches the list of currently airing top anime from Jikan API.
    """
    jikan = Jikan()
    anime_list = []
    error_message = None

    try:
        # 1. Call the top endpoint for 'anime' with filter 'airing'
        # The result is paginated, so we only fetch the first page (default)
        top_anime_data = jikan.top(type='anime', page=1,)
        
        # 2. The actual data is under the 'data' key in V4 of the Jikan API
        # We loop through the results to structure the data for the template
        for anime in top_anime_data.get('data', []):
            # The API response is a bit complex, so we carefully extract fields
            anime_details = {
                'id': anime.get('mal_id'),
                'title': anime.get('title'),
                'score': anime.get('score'),
                'episodes': anime.get('episodes'),
                'synopsis': anime.get('synopsis'),
                # Extract image URL from the nested 'images' dictionary
                'image_url': anime.get('images', {}).get('jpg', {}).get('image_url')
            }
            anime_list.append(anime_details)

    except Exception as e:
        # This catches API request failures or rate-limit errors
        error_message = f"Error fetching anime data: {e}"
        print(error_message)

    context = {
        'anime_list': anime_list,
        'error': error_message,
    }
    return render(request, 'anime/top_list.html', context)

# Example for a specific anime detail (e.g., /anime/detail/1)
def anime_details(request, mal_id):
    # First, get the local anime object
    local_anime = get_object_or_404(Anime, mal_id=mal_id)

    jikan = Jikan()
    context = {'local_anime': local_anime} # Start context with local data
    
    try:
        # Fetches a specific anime by its MyAnimeList ID
        response = jikan.anime(mal_id)
        api_data = response.get('data')

        if api_data:
            context['api'] = api_data

            # Save the poster URL from the API to our local anime object
            poster_url = api_data.get('images', {}).get('jpg', {}).get('large_image_url')
            if poster_url and local_anime.poster_api_url != poster_url:
                local_anime.poster_api_url = poster_url
                local_anime.save(update_fields=['poster_api_url'])
        else:
            context['api_error'] = "No data found for this anime in the API."

    except Exception as e:
        context['api_error'] = f"Could not connect to the anime database: {e}"
    
    return render(request, 'anime/detail.html', context)