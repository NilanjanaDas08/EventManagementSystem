from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Redirect to home for logged-in users
    path('post/',views.create_event,name="create_event"),
    path('event_list/',views.event_list,name="event_list"),
    path('search/',views.search,name="search"),   
    path('genres/<str:genre_name>/',views.get_genre,name="get_genre"),
    path(f'<int:event_id>/details',views.details,name="details"),   
]
