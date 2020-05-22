from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import * 

# Create your views here.

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm_Edited(request.POST)        
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            user = authenticate(username=username,password=password, email=email)
            messages.success(request, 'Account was created successfully!')
            return redirect("login")
    else:        
        form = UserCreationForm_Edited()

    context = {'form' : form}
    return render(request, 'accounts/register.html', context)

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = authenticate(username=username,password=password,email=email)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid user')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request):
    return render(request, 'accounts/index.html')

