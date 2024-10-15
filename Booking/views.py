from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Event,Booking,PaymentMethods
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required(login_url="login")
def book_ticket(request,event_id):
    context = {}
    context['signed_in'] = request.user.get_username()
    event = context['event'] = Event.objects.get(id=event_id)
    context['venue'] = event.venue_id
    context['payment_methods'] = PaymentMethods.objects.all()
    context['booking_id'] = Booking.objects.count() + 1
    context['time'] = timezone.now()

    if request.method=='POST':
        # payment_method_id=request.POST['payment_method']
        #Fetch the payment method
        # payment_method=get_object_or_404(PaymentMethods,id=payment_method_id)

        #Create Booking
        # booking=Booking.objects.create(
        #   user_id=request.user,
        #   event_id=event,
        #   no_of_seats_booked=no_of_seats_booked,
        #   payment=total_price,
        #   paid_using=payment_method
        #    )
        # return redirect('booking_confirm',booking_id=booking.id)
        
        no_of_seats_booked = request.session['no_of_seats_booked'] = int(request.POST['no_of_seats_booked'])
        request.session['total_price'] = request.POST['total_price']
        return redirect('select_payment_gateway',event_id)
    return render(request,'book_ticket.html',context)

@login_required(login_url="login")
def booking_confirm(request,booking_id):
    booking=get_object_or_404(Booking,id=booking_id)
    return render(request,'booking_confirm.html',{'booking':booking})


