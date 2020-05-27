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
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email address taken!')
                form = UserCreationForm_Edited()
            else:
                form.save()
                user = authenticate(username=username,password=password, email=email)                        
                project_member = Project_Member(user=user)
                project_member.save()
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
        user = authenticate(username=username,password=password)
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
    member = Project_Member.objects.get(user= request.user)
    projects = Project.objects.filter(project_members= member)
    context = {'projects':projects}
    return render(request, 'accounts/index.html', context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm(request.POST)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Project was created successfully!')            
        return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/createProject.html', context)


