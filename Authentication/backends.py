from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend
from django.http import HttpRequest

# Purpose: To use email as new validation

class EmailBackend(ModelBackend):
    """Authenticate using email and password"""
    
    def authenticate(self, request, email = None, password =  None, **kwargs: Any):
        try:
            User = get_user_model()
            user = User.objects.get(email = email)
        except Exception as e:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None