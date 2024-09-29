from django import forms 
from models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','date','start_time','end_time','posted_by','venue_id','status','price','created_at','updated_at']