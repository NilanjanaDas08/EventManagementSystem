from django import forms 
from django.contrib.auth.forms import UserCreationForm
from Authentication.models import User

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=('username','password')
