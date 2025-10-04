from django.urls import path
from . import views

urlpatterns = [
    path('', views.tvseries, name='tvseries'),
    path('<int:series_id>/', views.series_detail, name='series_detail'),
    path('api/season/<int:season_id>/episodes/', views.get_episodes_for_season, name='get_episodes_for_season'),
]
