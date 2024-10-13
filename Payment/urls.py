from django.urls import path
from . import views

urlpatterns=[
    path('payment/success/',views.payment_success_view.as_view(),name='payment-success'),
    path('payment/cancel/',views.payment_cancel_view.as_view(),name='payment-cancel')
               ]