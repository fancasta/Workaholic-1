from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from accounts.models import *

from .decorators import user_is_project_member, user_is_project_admin
from .forms import *
from todo.forms import *
from todo.models import Todo

# Create your views here.

@login_required
@user_is_project_member
def projectPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    admin_users = project.project_admin.all()
    admin_members = []
    for i in admin_users:
        admin_members.append(members.get(user=i))

    addMemberform = AddMemberForm(request.POST)
    
    if request.POST and addMemberform.is_valid:
        new_member = addMemberform.data['project_member']
        try:
            new_member_user = User.objects.get(username=new_member)
            member = Project_Member.objects.get(user=new_member_user)
            project.project_members.add(member)
            messages.info(request, str(member) + " added successfully!")
        except:
            messages.info(request,'Invalid user') 
            addMemberform = AddMemberForm()
    else:
        addMemberform = AddMemberForm()

    context = {'project':project, 'members':members, 'admin_members':admin_members, 'addMemberform':addMemberform, 'admin_users':admin_users}
    return render(request, 'project/home.html', context)


@login_required
@user_is_project_member
def addMembers(request,pk):
    pass
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

@login_required
@user_is_project_member
@user_is_project_admin
def deleteMember(request, pk, member_pk):
    project = Project.objects.get(id=pk)
    member = project.project_members.get(id=member_pk)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        project.project_members.remove(member)
        return redirect('/project/' + str(pk) + '/')
    else:
        deleteform = DeleteForm()

    context = {'project':project, 'member':member, 'deleteform': deleteform}
    return render(request, 'project/delete_member.html', context)


@login_required
@user_is_project_member
@user_is_project_admin
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        project.delete()
        return redirect('/')
    else:
        deleteform = DeleteForm()

    context = {'project':project, 'deleteform': deleteform}
    return render(request, 'project/delete_project.html', context)
