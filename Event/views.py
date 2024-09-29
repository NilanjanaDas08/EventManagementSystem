from django.shortcuts import render,redirect
from .forms import EventForm
from .models import Event

# Create your views here.
def index(request):
    return render(request,'index.html')

def create_event(request):
    if request.method=='POST':
        form=EventForm(request.POST)
        if form.is_valid():
            event=form.save(commit=False) #Not save the data in the database before it is posted
            event.posted_by=request.user  #User should be posted
            event.save()             # after that it will save to db
            return redirect('event_list')
        else:
            form=EventForm()
    return render(request,'create_event.html',{'form':form})

