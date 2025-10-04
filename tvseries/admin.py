from django.contrib import admin
from .models import TVSeries, Season, Episode

# Register your models here.
admin.site.register(TVSeries)
admin.site.register(Season)
admin.site.register(Episode)
