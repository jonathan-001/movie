from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True, 
        help_text="IMDb ID (e.g., tt1375666)")
    
    poster_api_url = models.URLField(
        max_length=500, 
        null=True, 
        blank=True,
        help_text="URL for the poster from OMDb API"
    )

    download_link = models.URLField(max_length=500, null=True, blank=True)
    watch_link = models.URLField(max_length=500, null=True, blank=True)

    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['title']
        verbose_name_plural = "Movies"
