from django.db import models
from django.utils import timezone

# Create your models here.
from django.db import models
from django.utils import timezone

class User(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    first_name = models.CharField(max_length=100) 
    middle_name=models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Ensures unique emails
    password = models.CharField(max_length=128)  # Stores hashed password
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
        ('GUEST', 'Guest'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('BANNED', 'Banned'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
class Venue(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    no_of_seats=models.IntegerField()
    VENUESTATUS_CHOICES=[
        ('ACTIVE','Active'),
        ('INACTIVE','Inactive'),
        ('UNDER_CONSTRUCTION','Under_construction'),
        ('CLOSED','Closed'),
    ]
    status=models.CharField(max_length=20,choices=VENUESTATUS_CHOICES,default='ACTIVE')
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return f"{self.name} ({self.location})-{self.get_status_display()}"
class Event(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    name=models.CharField(max_length=100)
    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    posted_by=models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    venue_id=models.ForeignKey(Venue,on_delete=models.CASCADE,null=True)
    EVENTSTATUS_CHOICES=[
     ('UPCOMING','UP'),
     ('ONGOING','ON'),
     ('COMPLETED','CO'),
     ('CANCELLED','CA'),]
    status=models.CharField(max_length=20,choices=EVENTSTATUS_CHOICES,default='UPCOMING')
    price=models.DecimalField(max_digits=10,decimal_places=2,null=True)
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.date})-{self.get_status_display()}"

class EventMedia(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
    file_name=models.CharField(max_length=100)
    FILETYPE_CHOICES=[
        ('IMAGE', 'Image'),
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio'),
        ('DOCUMENT', 'Document'),
        ]
    type=models.CharField(max_length=100,choices=FILETYPE_CHOICES,default='IMAGE')
    size=models.IntegerField()
    created_at=models.DateTimeField(auto_now=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.file_name} ({self.type})-{self.size}"
class Genre(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    name=models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.id} {self.name}"
class EventGenre(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
    genre_id=models.ForeignKey(Genre,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id} {self.genre_id}"
class PaymentMethods(models.Model):
    # id field is automatically created in Django as a primary key, so no need to explicitly define it.
    name=models.CharField(max_length=100)
    PAYMENTSTATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('PENDING', 'Pending'),
        ('REVOKED', 'Revoked'),
    ]
    status=models.CharField(max_length=20,choices=PAYMENTSTATUS_CHOICES,default='ACTIVE')

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

class Booking(models.Model):
     # id field is automatically created in Django as a primary key, so no need to explicitly define it.
     user_id=models.ForeignKey(User,on_delete=models.CASCADE)
     event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
     no_of_seats_booked=models.IntegerField()
     payment=models.DecimalField(max_digits=10,decimal_places=2)
     paid_using=models.ForeignKey(PaymentMethods,on_delete=models.CASCADE)
     created_at=models.DateTimeField(auto_now=True)
     updated_at=models.DateTimeField(auto_now=True)

     def __str__(self):
        return (f"Booking by {self.user_id.first_name} {self.user_id.last_name} "
                f"for {self.event_id.name} - {self.no_of_seats_booked} seats "
                f"paid using {self.paid_using.name} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")


    










    

