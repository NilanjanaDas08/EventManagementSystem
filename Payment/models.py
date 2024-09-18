from django.db import models

# Create your models here.
class PaymentMethods(models.Model):
    name=models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='ACTIVE')

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

