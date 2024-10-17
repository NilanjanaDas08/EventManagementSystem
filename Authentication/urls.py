from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('otp_verification/<str:username>/',views.otp_verification,name='otp_verification'),
    path('accounts/logout/', views.logout_view, name='logout'),

]
