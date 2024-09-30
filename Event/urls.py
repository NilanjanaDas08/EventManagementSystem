from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Redirect to home for logged-in users
    path('post/',views.create_event,name="create_event"),
]
