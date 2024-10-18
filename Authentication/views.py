from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserForm
from Event.models import Genre
from Authentication.models import User
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.cache import cache
import random

# Registration view
# NOTE: Need to render errors properly

def register(request):
    config = {}
    config['genres'] = Genre.objects.all()
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            config['form'] = form  # Sends errors correctly
    else:
        config['form'] = form  # Include an empty form for GET requests
    return render(request, 'registration/Register.html', config)

OTP_TIME_LIMIT = 600

def generate_otp():
    return random.randint(100000, 999999)

# Login view
def login_view(request):
    config = {}
    config['genres'] = Genre.objects.all()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        if user is not None:
            otp = generate_otp()
            # Store OTP in cache
            cache.clear()
            cache.delete(user)
            cache.set(user.id, otp, OTP_TIME_LIMIT)
            try:
                email = EmailMessage(
                    subject='Your OTP Code',
                    body=f'Your OTP code is {otp}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[f"{user.email}"],
                )
                email.send()
                return redirect('otp_verification', username=user.username)
            except Exception as e:
                messages.error("Failed to send OTP. Please try again.")
                return render(request, 'registration/login.html', config)
        else:
            messages.error(request, "Invalid credentials")
            config['error'] = "You have entered wrong username and/or password."
    return render(request, 'registration/login.html', config)

def otp_verification(request, username):
    user = User.objects.get(username=username)
    email = user.email
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        correct_otp = cache.get(user.id)

        if correct_otp is not None:
            if int(otp_entered) == correct_otp:
                login(request, user, backend = "Authentication.backends.EmailBackend")
                messages.success(request, f'Welcome, {username}!')
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, "Invalid OTP.")
        else:
            messages.error(request, "OTP has expired. Please request a new one.")
    else:
        messages.error(request, "No OTP generated for this user.")

    return render(request, 'registration/otp_verification.html', {'username': username, 'email': email})

# Logout view
def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))
