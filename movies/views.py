from django.shortcuts import render, get_object_or_404
from .models import Movie
from django.core.paginator import Paginator

# Create your views here.
def movies(request):
    movie_list = Movie.objects.all().order_by('title') # Order for consistent pagination
    paginator = Paginator(movie_list, 3) # Show 18 movies per page

    page_number = request.GET.get('page')
    movies_page = paginator.get_page(page_number)
    context = {
        'movies': movies_page
    }
    return render(request, 'movies.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    context = {
        'movie': movie
    }
    return render(request, 'movie_detail.html', context)
