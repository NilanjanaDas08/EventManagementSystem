from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    middle_name= models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
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
    # Add related_name to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Avoids conflict
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Avoids conflict
        blank=True,
    )
    def __str__(self):
        return f"{self.first_name} {self.last_name} Username: {self.username}"

