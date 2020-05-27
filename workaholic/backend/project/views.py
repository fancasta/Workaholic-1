from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from accounts.models import *

from .decorators import user_is_project_member

# Create your views here.

@login_required
@user_is_project_member
def projectPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    context = {'project':project, 'members':members}
    return render(request, 'project/home.html', context)
