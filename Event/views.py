from django.shortcuts import render,redirect
# from .forms import EventForm, EventMediaFormSet
from .forms import EventForm, EventMediaForm
from .models import Event,Genre
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    config = {}
    config['genres'] = Genre.objects.all()
    if request.user.is_authenticated == True:
        config['signed_in'] = request.user.get_username()
    return render(request, 'Home.html',config)

@login_required(login_url="login")
def create_event(request):
    form1 = EventForm()
    # form2 = EventMediaFormSet(queryset=EventMedia.objects.none())
    form2 = EventMediaForm()
    if request.method=='POST':
        form1 =EventForm(request.POST)
        # form2 = EventMediaFormSet(request.POST, request.FILES)
        form2 = EventMediaForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            event= form1.save(commit=False) #Not save the data in the database before it is posted
            event.posted_by=request.user  #User should be posted
            event.save()             # after that it will save to db

            form1.save_m2m() # Should save the genres passed in form, is not working properly, event is duplicating

            # for form in form2:
            #     image = form.save(commit=False)
            #     image.event_id = event
            #     image.save()
            
            image = form2.save(commit=False)
            image.event_id = event
            image.save()
            return redirect('event_list')
        else:
            form1=EventForm()
            # form2=EventMediaFormSet(queryset=EventMedia.objects.none())
            form2 = EventMediaForm()
    return render(request,'create_event.html',{'form1':form1, 'form2': form2, 'signed_in': request.user.get_username()})

def event_list(request):
    events=Event.objects.all()
    return render(request,'event_list.html',{'events':events})

def search(request):
    events = Event.objects.none()
    if request.method == "POST":
        event = request.POST['name']
        genre = request.POST['genre']
        
        # events = Event.objects.filter(name=event if event else None,genre=genre if genre else None)
        
        filter = Q()
        
        if event:
            filter &= Q(name__contains=event)
            
        if genre:
            filter &= Q(genres__name__contains = genre)
        
        events = Event.objects.filter(filter)
    return render(request,'event_list.html',{'events':events})

def get_genre(request, genre_name):
    events = Event.objects.filter(genres__name = genre_name)
    return render(request,'event_list.html',{'events':events})




