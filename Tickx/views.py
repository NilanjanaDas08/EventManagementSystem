from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect


# Create your views here.
@login_required
def Home(request):
    return render(request,'Registration/Home.html')
def Register(request):
    form = UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Successfull! Please log in')
            redirect('login')
        else:
            form=UserCreationForm()
    return render(request,'Registration/Register.html',{'form':form})
def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            redirect('home')    
        else:
            messages.error(request,"Invalid credentials")
    return render(request,'Registration/Login.html')

def Logout(request):
    logout(request)
    messages.success(request,"You have been logged out")
    return redirect('login')
def Profile(request):
    return render(request, 'accounts/Profile.html')
