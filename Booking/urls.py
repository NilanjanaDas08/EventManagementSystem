from django.urls import path
from . import views

urlpatterns=[
    path('book_ticket/<int:event_id>/',views.book_ticket,name='book_ticket'),
    path('booking_confirm/<int:booking_id>/',views.booking_confirm,name='booking_confirm'),
    ]