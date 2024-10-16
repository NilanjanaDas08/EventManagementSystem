from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from Authentication.models import User
from Event.models import Event
from Booking.models import Booking
from .models import PaymentMethods # At the moment not implemented properly, should represent different gateways like razorpay or stripe
from paypal.standard.forms import PayPalPaymentsForm
import uuid
import requests

# import paypalrestsdk
# from django.http import JsonResponse
# from .models import Booking,PaymentMethods
# from rest_framework import status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from Booking.views import book_ticket

# Configure Paypal SDK
# paypalrestsdk.configure({
#     'mode': settings.PAYPAL_MODE,
#     'client_id': settings.PAYPAL_CLIENT_ID,
#     'client_secret': settings.PAYPAL_CLIENT_SECRET
#        })

# class create_payment_view(APIView):
#     def post(self, request, booking_id):  #Handling POST requests
#         try:
#             booking = Booking.objects.get(id=booking_id)

#             # Calculate total payment amount based on the number of seats booked
#             total_payment = booking.no_of_seats_booked * booking.payment

#             payment = paypalrestsdk.Payment({
#                 "intent": "sale",
#                 "payer": {
#                     "payment_method": "paypal"
#                 },
#                 "redirect_urls": {
#                     "return_url": request.build_absolute_uri('/payment/success/'),
#                     "cancel_url": request.build_absolute_uri('/payment/cancel/')
#                 },
#                 "transactions": [{
#                     "amount": {
#                         "total": str(total_payment),  # Total amount to charge
#                         "currency": "INR"  
#                     },
#                     "description": f"Payment for {booking.no_of_seats_booked} tickets to {booking.event_id}."
#                 }]
#             })

#             if payment.create():
#                 # Returning approval URL for the client to proceed with PayPal payment
#                 return Response({'approval_url': payment['links'][1]['href']}, status=status.HTTP_200_OK)
#             else:
#                 # Return error details if payment creation failed
#                 return Response({'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)
        
#         except Booking.DoesNotExist:
#             return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)

# class payment_success_view(APIView):
#     def get(self, request):        #Handles get request
#         payment_id = request.GET.get('paymentId')
#         payer_id = request.GET.get('PayerID')

#         payment = paypalrestsdk.Payment.find(payment_id)

#         if payment.execute({"payer_id": payer_id}):
#             # Mark the booking as paid
#             booking_id = payment.transactions[0].description.split(' ')[-1]
#             booking = Booking.objects.get(id=booking_id)
#             booking.paid_using = PaymentMethods.objects.get(name='PayPal')  # Assuming PayPal is in PaymentMethods
#             booking.save()

#             return Response({'message': 'Payment successful', 'payment': payment.to_dict()}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Payment execution failed'}, status=status.HTTP_400_BAD_REQUEST)

# class payment_cancel_view(APIView):
#     def get(self, request):
#         return Response({'message': 'Payment canceled by the user'}, status=status.HTTP_200_OK)  

@login_required(login_url="login")
def select_payment_gateway(request,event_id):
    if 'no_of_seats_booked' not in request.session or 'total_price' not in request.session:
        return redirect(reverse('book_ticket', kwargs={'event_id':event_id}))

    context = {
        'event':Event.objects.get(id=event_id),
        'no_of_seats_booked':request.session.pop('no_of_seats_booked',None),
        'total_price':float(request.session.pop('total_price',None)),
        'payment_methods': PaymentMethods.objects.all(),
    }

    # Setting up PayPal payment (best if following setup as utils function)
    host = request.get_host()

    paypal_config = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': context['total_price'],
        'item_name': context['event'].name,
        'invoice': uuid.uuid4(), # Generates a random uuid for invoice
        'custom': f"{request.user.id}|{context['no_of_seats_booked']}",
        'currency_code': "USD",
        'notify_url': f"http://{host}{reverse('paypal-ipn')}", # We send all paypal configuration data to this url, paypal library handles the rest
        'return_url': f"http://{host}{reverse('payment_return', kwargs={'event_id': event_id})}", # Redirects to this url on success
        'cancel_url': f"http://{host}{reverse('payment_failure', kwargs={'event_id': event_id})}",
    }

    # Initializing PayPalPaymentsForm
    context['paypal'] = PayPalPaymentsForm(initial = paypal_config)

    return render(request,"payment_gateway_select.html",context)

@csrf_exempt
def payment_return(request, event_id):
    """Verifies Payment to Paypal and redirects to Booking Confirmation Page on Success"""

    # Get the 'PDT' token from PayPal
    pdt_token = request.GET.get('tx')  # This is the 'tx' parameter PayPal sends

    if not pdt_token:
        return HttpResponse("Payment failed", status=400)

    # Verify the PDT token with PayPal
    verify_response = verify_pdt(pdt_token)

    if verify_response.get('receiver_email') == settings.PAYPAL_RECEIVER_EMAIL.replace("@","%40",1) and \
        verify_response.get("payment_status") == "Completed": 

        # Payment is verified, process it
        event = Event.objects.get(id=event_id)
        user = User.objects.get(id = int(request.GET.get('custom').split("|")[0]))
        no_of_seats_booked = request.GET.get('custom').split("|")[1]
        booking = Booking.objects.create(
            user_id = user,
            event_id = event,
            no_of_seats_booked = no_of_seats_booked,
            payment = verify_response.get('mc_gross'),
            paid_using = PaymentMethods.objects.get(name="PayPal")  # Dynamic payment method
            # Shiould add a field for the generated invoice id
        )
        return redirect(reverse('booking_confirm', kwargs={'booking_id': booking.id}))
    
    # Payment not completed or failed
    return redirect(reverse('payment_failure', kwargs={'event_id': event_id}))

def verify_pdt(pdt_token):
    """Verify the PDT token with PayPal."""
    payload = {
        'cmd': '_notify-synch',
        'tx': pdt_token,
        'at': settings.PAYPAL_PDT_TOKEN  # This is the PDT token from your PayPal account
    }
    response = requests.post('https://www.sandbox.paypal.com/cgi-bin/webscr', data=payload) #Should remove sandbox for live testing

    # Log the full response text and status code for further inspection
    response_text = response.text

    # Parse the response, PayPal returns "SUCCESS" or "FAIL" followed by the transaction details
    response_data = response_text.split('\n')

    if response_data[0] == 'SUCCESS':
        pdt_info = dict(line.split('=') for line in response_data[1:] if '=' in line)
        return pdt_info
    
    return None

def payment_failure(request,event_id):
    event = Event.objects.get(id=event_id)
    return render(request,"payment_failure.html",{'event': event})