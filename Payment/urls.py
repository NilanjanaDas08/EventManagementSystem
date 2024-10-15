from django.urls import path
from . import views

urlpatterns=[
    path('<int:event_id>/payment/gateways',views.select_payment_gateway,name="select_payment_gateway"),
    path('<int:event_id>/payment/return/', views.payment_return, name='payment_return'),
    path('<int:event_id>/payment/cancel/',views.payment_failure,name='payment_failure'),
    # path('payment/success/',views.payment_success_view.as_view(),name='payment-success'),
    # path('payment/cancel/',views.payment_cancel_view.as_view(),name='payment-cancel'),
]