from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=255)
    
    release_date = models.DateField(null=True, blank=True)
    
    duration = models.IntegerField(
        null=True, 
        blank=True
    )
    
    country = models.CharField(
        max_length=100, 
        null=True, 
        blank=True
    )
    
    overview = models.TextField()
    
    genres = models.CharField(
        max_length=255
    )
    
    cast_members = models.TextField()
    
    production = models.TextField(
        null=True, 
        blank=True
    )
    
    imdb_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        null=True, 
        blank=True
    )
    
    poster_image = models.ImageField(
        upload_to='posters/', 
        null=True, 
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-release_date', 'title']
        verbose_name_plural = "Movies"
