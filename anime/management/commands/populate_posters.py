import time
from django.core.management.base import BaseCommand
from anime.models import Anime
from django.db.models import Q
from jikanpy import Jikan

class Command(BaseCommand):
    help = 'Fetches and populates poster URLs for anime that are missing them.'

    def handle(self, *args, **options):
        jikan = Jikan()
        
        # Find all anime objects where the poster_api_url is null or an empty string
        anime_to_update = Anime.objects.filter(Q(poster_api_url__isnull=True) | Q(poster_api_url='')).only('id', 'mal_id', 'title')
        
        if not anime_to_update.exists():
            self.stdout.write(self.style.SUCCESS('All anime entries already have poster URLs. Nothing to do.'))
            return

        self.stdout.write(f'Found {anime_to_update.count()} anime to update.')

        for anime in anime_to_update:
            self.stdout.write(f'Fetching data for "{anime.title}" (MAL ID: {anime.mal_id})...')
            try:
                response = jikan.anime(anime.mal_id)
                api_data = response.get('data')

                if api_data:
                    poster_url = api_data.get('images', {}).get('jpg', {}).get('large_image_url')
                    if poster_url:
                        anime.poster_api_url = poster_url
                        # Also update the title if it's a placeholder
                        if not anime.title or anime.title.startswith('Anime ID'):
                            anime.title = api_data.get('title_english') or api_data.get('title')
                        
                        anime.save()
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated poster for "{anime.title}".'))
                    else:
                        self.stdout.write(self.style.WARNING(f'No poster URL found in API response for "{anime.title}".'))
                
                # Jikan API has a rate limit (e.g., 3 requests per second). A small delay is good practice.
                time.sleep(1) # Sleep for 1 second between requests

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'Failed to fetch data for MAL ID {anime.mal_id}: {e}'))
        
        self.stdout.write(self.style.SUCCESS('Finished updating anime posters.'))