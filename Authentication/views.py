from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def home(request):
    return render(request, 'registration/Home.html')

# Registration view
def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Fixed redirect to work properly
    return render(request, 'registration/Register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Fixed redirect to work properly
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'registration/Login.html')

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('login')

# Profile view (example)
@login_required
def profile(request):
    return render(request, 'accounts/Profile.html')
