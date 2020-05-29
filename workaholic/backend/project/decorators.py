from django.http import HttpResponse
from django.shortcuts import redirect

from accounts.models import *

def user_is_project_member(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        user = Project_Member.objects.get(user= request.user)
        members = project.project_members.all()

        if user in members:
            return function(request,  *args, **kwargs)
        else:
            return redirect('/')
    return wrap

def user_is_project_admin(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        if request.user == project.project_admin:
            return function(request,  *args, **kwargs)
        else:
            return redirect('/project/' + str(kwargs['pk']) + '/')
    return wrap
