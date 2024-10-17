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
from .utils import verify_pdt
from uuid import uuid4,UUID

@login_required(login_url="login")
def select_payment_gateway(request,event_id):
    if 'no_of_seats_booked' not in request.session or 'total_price' not in request.session:
        return redirect(reverse('book_ticket', kwargs={'event_id':event_id}))

    # Ensuring unique invoice id
    while True:
        invoice_id = uuid4()
        if Booking.objects.filter(invoice_id = invoice_id).count() == 0:
            break

    context = {
        'event':Event.objects.get(id=event_id),
        'no_of_seats_booked':request.session.pop('no_of_seats_booked',None),
        'total_price':float(request.session.pop('total_price',None)),
        'payment_methods': PaymentMethods.objects.all(),
        'invoice_id': invoice_id
    }

    # Setting up PayPal payment (best if following setup as utils function)
    host = request.get_host()

    paypal_config = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': context['total_price'],
        'item_name': context['event'].name,
        'invoice': str(invoice_id),
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
        invoice_id = UUID(request.GET.get('invoice'))

        booking = Booking.objects.create(
            user_id = user,
            event_id = event,
            no_of_seats_booked = no_of_seats_booked,
            payment = verify_response.get('mc_gross'),
            paid_using = PaymentMethods.objects.get(name="PayPal"),  # Dynamic payment method
            invoice_id = invoice_id,
        )

        # To make sure we cannot reach booking confirm page again
        request.session['booking'] = True

        return redirect(reverse('booking_confirm', kwargs={'booking_id': booking.id}))
    
    # Payment not completed or failed
    return redirect(reverse('payment_failure', kwargs={'event_id': event_id}))

def payment_failure(request,event_id):
    event = Event.objects.get(id=event_id)
    return render(request,"payment_failure.html",{'event': event})