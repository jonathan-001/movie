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

def anime_search_view(request):
    query = request.GET.get('q', '')
    results = []
    error_message = None
    jikan = Jikan()

    if query:
        try:
            search_result = jikan.search('anime', query)
            results = search_result.get('data', [])
        except Exception as e:
            error_message = f"Error searching for anime: {e}"

    context = {
        'query': query,
        'results': results,
        'error': error_message
    }
    return render(request, 'anime/search_results.html', context)

def top_airing_anime(request):
    """
    Fetches the list of currently airing top anime from Jikan API.
    """
    jikan = Jikan()
    anime_list = []
    error_message = None

    try:
        # 1. Call the top endpoint for 'anime' with filter 'airing'
        top_anime_data = jikan.top(type='anime', page=1,)
        
        # 2. The actual data is under the 'data' key in V4 of the Jikan API
        api_results = top_anime_data.get('data', [])

        for item in api_results:
            mal_id = item.get('mal_id')
            if not mal_id:
                continue

            # Use update_or_create to add new anime or update existing ones
            anime_obj, created = Anime.objects.update_or_create(
                mal_id=mal_id,
                defaults={
                    'title': item.get('title_english') or item.get('title'),
                    'poster_api_url': item.get('images', {}).get('jpg', {}).get('large_image_url')
                }
            )
            # We pass the API data directly to the template for immediate display
            anime_list.append(item)

    except Exception as e:
        # This catches API request failures or rate-limit errors
        error_message = f"Error fetching anime data: {e}"
        print(error_message)

    context = {
        'anime_list': anime_list,
        'error': error_message
    }
    return render(request, 'anime/top_list.html', context)

# Example for a specific anime detail (e.g., /anime/detail/1)
def anime_details(request, mal_id):
    # Use get_or_create. This is the key change.
    # It tries to find an anime with the given mal_id.
    # If it doesn't exist, it creates a new Anime object in the database.
    # 'created' is a boolean that tells us if a new object was made.
    local_anime, created = Anime.objects.get_or_create(
        mal_id=mal_id,
        defaults={'title': f'Anime ID {mal_id}'} # A temporary title
    )

    jikan = Jikan()
    context = {'local_anime': local_anime} # Start context with local data
    
    try:
        # Fetches a specific anime by its MyAnimeList ID
        response = jikan.anime(mal_id)
        api_data = response.get('data')

        if api_data:
            context['api'] = api_data

            # If the local title is the temporary one, update it with the real title
            english_title = api_data.get('title_english')
            main_title = api_data.get('title')
            if local_anime.title == f'Anime ID {mal_id}' or created:
                local_anime.title = english_title or main_title

            # Save the poster URL from the API to our local anime object
            poster_url = api_data.get('images', {}).get('jpg', {}).get('large_image_url')
            if poster_url and local_anime.poster_api_url != poster_url:
                local_anime.poster_api_url = poster_url
                local_anime.save(update_fields=['poster_api_url'])
        else:
            # If the API fails but we just created a local object, it's better to delete it
            # to avoid having a permanent empty entry in the database.
            if created:
                local_anime.delete()
            context['api_error'] = "No data found for this anime in the API."

    except Exception as e:
        context['api_error'] = f"Could not connect to the anime database: {e}"
    
    return render(request, 'anime/detail.html', context)