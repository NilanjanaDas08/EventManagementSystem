from django.db import models
from Authentication.models import User

# Create your models here.
class Venue(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    no_of_seats=models.IntegerField()
    STATUS_CHOICES=[
        ('ACTIVE','Active'),
        ('INACTIVE','Inactive'),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='ACTIVE')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"{self.name} at {self.location} with {self.no_of_seats} seats - status: {self.get_status_display()}"

class Genre(models.Model):
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name}"

class Event(models.Model):
    name=models.CharField(max_length=100)
    date=models.DateField()
    details = models.TextField(default=None)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()

    # These fields should not be null, they are set to null to avoid migration errors, ensure proper data entry
    posted_by=models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE) 
    venue_id=models.ForeignKey(Venue,null=True,blank=True,on_delete=models.CASCADE)
    
    # Could consider simplifying it for sake of simplicity, otherwise these choices work
    STATUS_CHOICES=[
     ('UPCOMING','UP'),
     ('ONGOING','ON'),
     ('COMPLETED','CO'),
     ('CANCELLED','CA'),]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='UPCOMING')
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True)

    genres = models.ManyToManyField(Genre, related_name="events", blank=True) # An event can have multiple genres, and vice versa

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def get_media(self):
        return EventMedia.objects.filter(event_id = self)

    def __str__(self):
        return f"{self.name} on {self.date} from {self.start_time} to {self.end_time} - Status: {self.get_status_display()}"


class EventMedia(models.Model):
    event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
    # file_name=models.CharField(max_length=100)
    TYPE_CHOICES=[
        ('BANNER', 'banner'),
        ('DETAIL', 'detail'),
    ]
    type=models.CharField(max_length=100,choices=TYPE_CHOICES,default='banner')
    image = models.ImageField(upload_to='images/', height_field=None, width_field=None, max_length=None)
    # size=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.image.name} ({self.type})-{self.image.size}"
    
# class EventGenre(models.Model):
#     event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
#     genre_id=models.ForeignKey(Genre,on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.id} {self.genre_id}"

