from django.contrib import admin
from .models import TVSeries, Season, Episode

class EpisodeInline(admin.StackedInline):
    model = Episode
    extra = 1
    # The readonly_fields will prevent errors since 'series' is auto-populated.
    readonly_fields = ('series',)

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    inlines = [EpisodeInline]
    list_display = ('name', 'series', 'release_date')
    list_filter = ('series',)

class SeasonInline(admin.TabularInline):
    model = Season
    extra = 1

@admin.register(TVSeries)
class TVSeriesAdmin(admin.ModelAdmin):
    inlines = [SeasonInline]
    list_display = ('title', 'release_date', 'country', 'imdb_rating')
    search_fields = ('title',)
