from django.shortcuts import render
import paypalrestsdk
from django.conf import settings
from django.http import JsonResponse
from .models import Booking,PaymentMethods
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from Booking.views import book_ticket

# Configure Paypal SDK
paypalrestsdk.configure({
    'mode': settings.PAYPAL_MODE,
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET
       })

class create_payment_view(APIView):
    def post(self, request, booking_id):  #Handling POST requests
        try:
            booking = Booking.objects.get(id=booking_id)

            # Calculate total payment amount based on the number of seats booked
            total_payment = booking.no_of_seats_booked * booking.payment

            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": request.build_absolute_uri('/payment/success/'),
                    "cancel_url": request.build_absolute_uri('/payment/cancel/')
                },
                "transactions": [{
                    "amount": {
                        "total": str(total_payment),  # Total amount to charge
                        "currency": "INR"  
                    },
                    "description": f"Payment for {booking.no_of_seats_booked} tickets to {booking.event_id}."
                }]
            })

            if payment.create():
                # Returning approval URL for the client to proceed with PayPal payment
                return Response({'approval_url': payment['links'][1]['href']}, status=status.HTTP_200_OK)
            else:
                # Return error details if payment creation failed
                return Response({'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)
        
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

class payment_success_view(APIView):
    def get(self, request):        #Handles get request
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            # Mark the booking as paid
            booking_id = payment.transactions[0].description.split(' ')[-1]
            booking = Booking.objects.get(id=booking_id)
            booking.paid_using = PaymentMethods.objects.get(name='PayPal')  # Assuming PayPal is in PaymentMethods
            booking.save()

            return Response({'message': 'Payment successful', 'payment': payment.to_dict()}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment execution failed'}, status=status.HTTP_400_BAD_REQUEST)

class payment_cancel_view(APIView):
    def get(self, request):
        return Response({'message': 'Payment canceled by the user'}, status=status.HTTP_200_OK)  