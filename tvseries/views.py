from django.shortcuts import render

# Create your views here.
def tvseries(request):
    return render(request, 'tv-series.html')