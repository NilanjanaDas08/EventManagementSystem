from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserForm
from Event.models import Genre
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
import random
import time

# Registration view
<<<<<<< HEAD
=======
# NOTE: Need to account for other additional fields
# NOTE: Need to render errors properly

>>>>>>> 0a799ccdaa0052883c1045ff385b1a4f116347f4
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
<<<<<<< HEAD
            otp = generate_otp()
            # Store OTP in cache
            cache.set(username, otp, OTP_TIME_LIMIT)
            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('otp_verification', username=username)
            except Exception as e:
                messages.error(request, "Failed to send OTP. Please try again.")
                return render(request, 'registration/login.html', config)
        else:
            messages.error(request, "Invalid credentials")
            config['error'] = "You have entered wrong username and/or password."
    return render(request, 'registration/login.html', config)

def otp_verification(request, username):
    if request.method == 'POST':
        otp_entered = request.POST['otp']
        correct_otp = cache.get(username)
        current_time = time.time()

        if correct_otp is not None:
            if int(otp_entered) == correct_otp:
                login(request, authenticate(request, username=username))
                messages.success(request, f'Welcome, {username}!')
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, "Invalid OTP.")
        else:
            messages.error(request, "OTP has expired. Please request a new one.")
    else:
        messages.error(request, "No OTP generated for this user.")

    return render(request, 'registration/otp_verification.html', {'username': username})
=======
            login(request, user)
            messages.success(request,f'Welcome,{email}!')
            
            next_url = request.GET.get('next','/')
            if next_url: return redirect(next_url);
            # return redirect('home')  # Fixed redirect to work properly
        else:
            messages.error(request, "Invalid credentials")
            config['error'] = "You have entered wrong email and/or password."
    return render(request, 'registration/login.html',config)
>>>>>>> 0a799ccdaa0052883c1045ff385b1a4f116347f4

# Logout view
def logout_view(request):
    logout(request)
    return redirect(request.GET.get('next', '/'))
