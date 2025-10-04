from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies, name='movies'),
    path('<int:movie_id>/', views.movie_detail, name='movie_detail'),
]
