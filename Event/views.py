from django.shortcuts import render,redirect
# from .forms import EventForm, EventMediaFormSet
from .forms import EventForm, EventMediaForm
from .models import Event,Genre
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):
    config = {}
    config['genres'] = Genre.objects.all()[:5]

    # Handling Home Page events
    latest_events = Event.objects.filter(status = "UPCOMING").order_by("-id")
    config['events_trending'] = latest_events[:5]
    config['events_swipper'] = latest_events[5:10]
    config['random_genre'] = random_genre = Genre.objects.order_by("?").first()
    config['events_section'] = latest_events.filter(genres = random_genre)

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
    events=Event.objects.filter(status='UPCOMING').prefetch_related('genres')
    paginator=Paginator(events,6)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    genres=Genre.objects.all()
    return render(request,'event_list.html',{'events':events, 'genres': genres,'page_obj':page_obj, 'signed_in': request.user.get_username()})

def search(request):
    events = Event.objects.none()
    genres = Genre.objects.all()
    search_query=[]
    if request.method=="GET":
        event=request.GET.get('name').strip() if request.GET.get('name') else None
        genre=request.GET.get('genre').strip() if request.GET.get('genre') else None
         # events = Event.objects.filter(name=event if event else None,genre=genre if genre else None)

        filter = Q(status='UPCOMING')
        
        if event:
            filter &= Q(name__contains=event)
            search_query.append(event)

        if genre:
            filter &= Q(genres__name__contains = genre)
            search_query.append(genre)
        
        events = Event.objects.filter(filter)
        paginator=Paginator(events,6)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)

    return render(request,'event_list.html',{'events':events,'page_obj':page_obj, 'search_query': " & ".join(search_query),'genres': genres, 'signed_in': request.user.get_username()})

def get_genre(request, genre_name):
    events = Event.objects.filter(genres__name = genre_name)
    genres = Genre.objects.all()
    paginator=Paginator(events,6)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'event_list.html',{'events':events, 'genres': genres, 'genre_name': genre_name,'page_obj':page_obj, 'signed_in': request.user.get_username()})

def details(request, event_id):
    config = {}
    config['event'] = Event.objects.get(id = event_id)
    config['related_events'] = Event.objects.filter(genres__name = config['event'].genres.first()).exclude(id = event_id)[:3] # Need to limit this

    config['signed_in'] = request.user.get_username()
    config['genres'] = Genre.objects.all()

    return render(request, 'details.html', config)

'''def search(request):
    events=Event.objects.none()
    genres=Genre.objects.all()
    search_query=[]
    if request.method=='GET':
        event=request.GET.get('name','').strip()
        genre=request.GET.get('genre','').strip()
        filter_criteria={'status':'UPCOMING'}              Nilanjana
        if event:
            filter_criteria['name__icontains']=event
            search_query.append(event)
        if genre:
            filter_criteria['genres__name__icontains']=genre
            search_query.append(genre)
        events=Event.objects.filter(**filter_criteria)
    return render(request,'event_list.html',{'events':events, 'search_query': search_query,'genres': genres, 'signed_in': request.user.get_username()})'''

