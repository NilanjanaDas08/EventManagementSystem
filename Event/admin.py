from django.contrib import admin
from .models import Event,EventMedia,Genre,Venue

# Register your models here.
admin.site.register(Event)
admin.site.register(EventMedia)
admin.site.register(Genre)
admin.site.register(Venue)