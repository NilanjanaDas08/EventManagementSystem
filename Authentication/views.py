from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserForm

# Registration view
# NOTE: Need to account for other additional fields
def register(request):
    config = {}
    form = config['form'] = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')  # Fixed redirect to work properly
        else: 
            # print(form.errors)
            # str = form.errors.as_text()
            # config['error'] = str[str.find("*",str.find("*")+1)+1:] # Logging Registration Form Error
            config['form'] = form # Sends errors correctly
    return render(request, 'registration/Register.html', config)

# Login view
def login_view(request):
    config = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,f'Welcome,{username}!')
            
            next_url = request.GET.get('next','/')
            if next_url: return redirect(next_url);
            return redirect('home')  # Fixed redirect to work properly
        else:
            messages.error(request, "Invalid credentials")
            config['error'] = "You have entered wrong username and/or password."
    return render(request, 'registration/login.html',config)

# Logout view
def logout_view(request):
    logout(request)
    # messages.success(request, "You have been logged out")
    return redirect('home')

''''# Profile view (example)
@login_required
def profile(request):
    return render(request, 'accounts/Profile.html')'''
