from django.contrib import admin
from .models import Anime, AnimeWatchLink


class AnimeWatchLinkInline(admin.TabularInline):
    """
    Allows editing of watch links directly within the Anime admin page.
    This provides a more intuitive interface than managing them separately.
    """
    model = AnimeWatchLink
    extra = 1  # Provides 1 extra empty form for a new link by default.
    fields = ('name', 'url')

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Anime model.
    """
    # Adds a search bar to the admin list page that searches the specified fields.
    search_fields = ['title', 'mal_id']

    # Defines the columns shown in the admin list view for a cleaner look.
    list_display = ('title', 'mal_id')

    # Embeds the watch link form directly into the Anime change page.
    inlines = [AnimeWatchLinkInline]