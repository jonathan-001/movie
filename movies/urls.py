from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.movies, name='movies'),
    path('search/', views.search_view, name='search'),
    path('<str:imdb_id>/', views.movie_detail_view, name='movie_detail'),
]
