from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from accounts.models import *

from .decorators import user_is_project_member
from .forms import *

# Create your views here.

@login_required
@user_is_project_member
def projectPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    context = {'project':project, 'members':members}
    return render(request, 'project/home.html', context)

@login_required
@user_is_project_member
def addMembers(request,pk):
    project = Project.objects.get(id=pk)
    form = AddMemberForm(request.POST)
    if request.POST and form.is_valid:
        new_member = form.data['project_member']
        try:
            new_member_user = User.objects.get(username=new_member)
            member = Project_Member.objects.get(user=new_member_user)
            project.project_members.add(member)
            messages.info(request, str(member) + " added successfully!")
        except:
            messages.info(request,'Invalid user') 
            form = AddMemberForm()
        
    else:
        form = AddMemberForm()
    
    context = {'form':form, 'project':project}
    return render(request, 'project/add_members.html', context)