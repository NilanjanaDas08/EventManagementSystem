from django.shortcuts import render,redirect
from .forms import EventForm, EventMediaFormSet
from .models import Event, EventMedia
from django.contrib.auth.decorators import login_required

def home(request):
    config = {}
    if request.user.is_authenticated == True:
        config['signed_in'] = request.user.get_username()
    return render(request, 'Home.html',config)

@login_required(login_url="login")
def create_event(request):
    form1 = EventForm()
    form2 = EventMediaFormSet(queryset=EventMedia.objects.none())
    if request.method=='POST':
        form1 =EventForm(request.POST)
        form2 = EventMediaFormSet(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            event= form1.save(commit=False) #Not save the data in the database before it is posted
            event.posted_by=request.user  #User should be posted
            event.save()             # after that it will save to db

            form1.save_m2m() # Should save the genres passed in form, is not working properly, event is duplicating

            for form in form2:
                image = form.save(commit=False)
                image.event_id = event
                image.save()
            return redirect('event_list')
        else:
            form1=EventForm()
            form2=EventMediaFormSet(queryset=EventMedia.objects.none())
    return render(request,'create_event.html',{'form1':form1, 'form2': form2, 'signed_in': request.user.get_username()})

def event_list(request):
    events=Event.objects.all()
    return render(request,'event_list.html',{'events':events})

