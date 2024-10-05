from typing import Any
from django.core.management.base import BaseCommand
from Event.models import Event,Genre,Venue,EventMedia
from Authentication.models import User
import os

class Command(BaseCommand):
    help = "Clearing Seeded Data From All Event Models"

    def handle(self, *args: Any, **options: Any):
        self.stdout.write(self.style.SUCCESS("Deleting Seeded Data......."))

        # Deleting Event Media (to avoid Foreign Key Conflicts)
        event_media_files = EventMedia.objects.all()
        for media in event_media_files:
            image_path = media.image.path
            if os.path.isfile(image_path):
                os.remove(image_path)
                self.stdout.write(f"Deleted image from {image_path}")
            media.delete()
        self.stdout.write(self.style.SUCCESS("Deleted Event Media Files!"))

        # Deleting Events
        Event.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Deleted Events!"))

        # Deleting Non-SuperUsers
        User.objects.exclude(is_superuser = True).delete()
        self.stdout.write(self.style.SUCCESS("Deleted Non-Super Users!"))

        # Deleting Genres
        Genre.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted Genres!'))

        # Deleting Venues
        Venue.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted Venues!'))

        self.stdout.write(self.style.SUCCESS("ALL DATA (except superusers) DELETED!"))