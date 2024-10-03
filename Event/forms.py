from django import forms 
from .models import Event,EventMedia

class EventForm(forms.ModelForm):
    class Meta:
        model=Event
        fields=['name','date','details','genres','start_time','end_time','venue_id','price']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date input
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # HTML5 datetime-local input
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class EventMediaForm(forms.ModelForm):
    class Meta:
        model = EventMedia
        fields = ['type','image']