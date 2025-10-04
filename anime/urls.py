from django.urls import path
from . import views

app_name = 'anime'

urlpatterns = [
    path('', views.anime, name='anime'),
    path('top/', views.top_airing_anime, name='top_anime'),
    path('detail/<int:mal_id>/', views.anime_details, name='anime_detail'),
]