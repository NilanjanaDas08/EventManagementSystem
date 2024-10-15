from django.db import models
from Authentication.models import User
from Event.models import Event
from Payment.models import PaymentMethods

# Create your models here.
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
        return (f"Booking by {self.user_id.username} "
                f"for {self.event_id.name} - {self.no_of_seats_booked} seats "
                f"paid using {self.paid_using.name} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
