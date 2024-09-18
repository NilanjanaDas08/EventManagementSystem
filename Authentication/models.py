from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

# id field is automatically created in Django as a primary key, so no need to explicitly define it in any class.

class User(models.Model):
    first_name = models.CharField(max_length=255) 
    middle_name= models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)  # Ensures unique emails
    password = models.CharField(max_length=255)  # Stores hashed password
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'), 
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

