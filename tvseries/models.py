from django.db import models

# Create your models here.

class TVSeries(models.Model):
    title = models.CharField(max_length=255, verbose_name="Series Title")
    overview = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    poster_image = models.ImageField(upload_to='series_posters/', null=True, blank=True)
    download_link = models.URLField(max_length=500, null=True, blank=True)
    watch_link = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "TV Series"
        ordering = ['title']

class Season(models.Model):
    series = models.ForeignKey(
        TVSeries, 
        on_delete=models.CASCADE, 
        related_name='seasons'
    )
    season_number = models.IntegerField()
    name = models.CharField(max_length=255, verbose_name="Season Name")
    release_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.series.title} - Season {self.season_number}: {self.name}"

    class Meta:
        unique_together = ('series', 'season_number')
        ordering = ['series', 'season_number']

class Episode(models.Model):
    season = models.ForeignKey(
        Season, 
        on_delete=models.CASCADE, 
        related_name='episodes'
    )
    episode_number = models.IntegerField()
    title = models.CharField(max_length=255, verbose_name="Episode Title")
    air_date = models.DateField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, verbose_name="Duration (minutes)")

    def __str__(self):
        return f"S{self.season.season_number}E{self.episode_number}: {self.title}"

    class Meta:
        unique_together = ('season', 'episode_number')
        ordering = ['season', 'episode_number']
