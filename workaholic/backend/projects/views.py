from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .decorators import user_is_project_member

from accounts.models import *

@login_required
@user_is_project_member
def projectPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    context = {'project':project, 'members':members}
    return render(request, 'project/home.html', context)
