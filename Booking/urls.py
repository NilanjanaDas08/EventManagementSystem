from django.urls import path
from . import views

urlpatterns=[
    path('<int:event_id>/book_ticket/',views.book_ticket,name='book_ticket'),
    path('booking_confirm/<int:booking_id>/',views.booking_confirm,name='booking_confirm'),
    path('booking_confirm/<int:booking_id>/pdf',views.serve_pdf,name="serve_pdf"),
]