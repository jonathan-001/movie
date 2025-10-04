from django.db import models

# Create your models here.
class Anime(models.Model):
    mal_id = models.IntegerField(unique=True, help_text="MyAnimeList ID")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster = models.ImageField(upload_to='anime_posters/', blank=True, null=True)
    poster_api_url = models.URLField(max_length=500, blank=True, null=True)
    trailer_link = models.URLField(blank=True, null=True)
    # Add any other local-only fields you need

    def __str__(self):
        return self.title