from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.tvseries, name='tvseries'),
]
