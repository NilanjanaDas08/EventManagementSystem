from django.shortcuts import render,redirect,get_object_or_404
from .models import Event,Booking,PaymentMethods
from Event.models import Genre
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .utils import generate_qr_code, render_pdf_view
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.conf import settings

@login_required(login_url="login")
def book_ticket(request,event_id):
    context = {}
    context['signed_in'] = request.user.get_username()
    event = context['event'] = Event.objects.get(id=event_id)
    context['venue'] = event.venue_id
    context['payment_methods'] = PaymentMethods.objects.all()
    context['time'] = timezone.now()

    if request.method=='POST':
        request.session['no_of_seats_booked'] = int(request.POST['no_of_seats_booked'])
        request.session['total_price'] = request.POST['total_price']
        return redirect('select_payment_gateway',event_id)
    return render(request,'book_ticket.html',context)

@login_required(login_url="login")
def booking_confirm(request,booking_id):
    """Booking Confirmation Page"""

    if 'booking' not in request.session:
        return HttpResponse("Please go back to Tickx to book properly",status = 400)
    
    del request.session['booking']
    user = request.user
    media_url = settings.MEDIA_URL

    booking = get_object_or_404(Booking,id=booking_id)
    context = {
        'signed_in': user.get_username(),
        'booking': booking,
        'event': Event.objects.get(id = booking.event_id.id),
        'qr_code': generate_qr_code(str(booking.invoice_id)),
        'media_url': media_url,
        'genres': Genre.objects.all()[:5],
    }
    context['related_events'] = Event.objects.filter(genres__name = context['event'].genres.first()).exclude(id = context['event'].id)[:5]

    subject = f"Tickx - Booking for {context['event'].name} confirmed"
    body = f"You have successfully booked your event for {context['event'].name} on" + \
            f"{context['event'].date} at {context['event'].venue_id.name},{context['event'].venue_id.location} from" + \
            f"{context['event'].start_time.strftime('%H:%m %p')} to {context['event'].end_time.strftime('%H:%m %p')}." + \
            f"Please check attachment for your ticket!"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [f"{user.email}"]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email = from_email,
        to = to_email
    )

    pdf_config = {
        'booking': booking,
        'event': Event.objects.get(id = booking.event_id.id),
        'qr_code': generate_qr_code("https://www.tickx.com/"+str(booking.invoice_id))
    }

    pdf = render_pdf_view(request,pdf_config)
    email.attach(f"{booking.user_id.username} - Ticket for {booking.event_id.name}",pdf.read(),"application/pdf")
    email.send()

    return render(request,'booking_confirm.html',context)

@login_required(login_url="login")
def serve_pdf(request, booking_id):
    """Download Ticket Option"""
    # NOTE: Not the most efficient way, could store pdf in local to access faster

    username = request.user.get_username()
    booking = get_object_or_404(Booking,id=booking_id)
    pdf_config = {
        'booking': booking,
        'event': Event.objects.get(id = booking.event_id.id),
        'qr_code': generate_qr_code("https://www.tickx.com/"+str(booking.invoice_id))
    }

    pdf = render_pdf_view(request,pdf_config)
    response = HttpResponse(pdf,"application/pdf")
    response['Content-Disposition'] = f"inline; filename='{username}_{pdf_config['event'].name}_{booking.created_at}.pdf'"

    return response

