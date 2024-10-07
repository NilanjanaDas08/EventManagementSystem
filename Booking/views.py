from django.shortcuts import render,redirect,get_object_or_404
from .models import User,Event,Booking,PaymentMethods
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def book_ticket(request,event_id):
    event=Event.objects.get(id=event_id)
    payment_methods=PaymentMethods.objects.all()

    if request.method=='POST':
        no_of_seats_booked=int(request.POST['no_of_seats_booked'])
        payment_method_id=request.POST['payment_method']

        #Fetch the payment method
        payment_method=get_object_or_404(PaymentMethods,id=payment_method_id)
        total_price=no_of_seats_booked*event.price
        #Create Booking
        booking=Booking.objects.create(
          user_id=request.user,
          event_id=event,
          no_of_seats_booked=no_of_seats_booked,
          payment=total_price,
          paid_using=payment_method
           )
        return redirect('booking_confirm',booking_id=booking.id)
    return render(request,'book_ticket.html',{'event':event,'payment_methods':payment_methods})

@login_required
def booking_confirm(request,booking_id):
    booking=get_object_or_404(Booking,id=booking_id)
    return render(request,'booking_confirm.html',{'booking':booking})


