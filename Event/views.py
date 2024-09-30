from django.shortcuts import render,redirect
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required

def home(request):
    config = {}
    if request.user.is_authenticated == True:
        config['signed_in'] = request.user.get_username()
    return render(request, 'Home.html',config)

@login_required(login_url="login")
def create_event(request):
    form = EventForm()
    if request.method=='POST':
        form=EventForm(request.POST)
        if form.is_valid():
            event=form.save(commit=False) #Not save the data in the database before it is posted
            event.posted_by=request.user  #User should be posted
            event.save()             # after that it will save to db
            return redirect('event_list')
        else:
            print(form.errors)
            form=EventForm()
    return render(request,'create_event.html',{'form':form, 'signed_in': request.user.get_username()})

