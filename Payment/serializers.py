from rest_framework import serializers
from .models import Booking,PaymentMethods
class PaymentSerializer(serializers.Serializer):
    booking_id=serializers.IntegerField()      #Representing booking id
    no_of_seats_booked=serializers.IntegerField()  # Representing No of seats booked

    def create(self,validated_data)
    # This method handles the creation of the booking based on the validated data from the request.
    booking_instance = Booking.objects.get(id=validated_data['booking_id'])  # Fetch booking by ID.
    return booking_instance
