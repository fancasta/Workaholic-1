from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator #import Paginator

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import datetime
# Create your views here.
from accounts.models import *

from .decorators import user_is_project_member, user_is_project_admin
from .forms import *
from todo.forms import *
from todo.models import Todo
from board.models import Board
from cal.models import Event
from forum.models import Thread

# Create your views here.

@login_required
@user_is_project_member
def projectPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    admin_users = project.project_admin.all()
    admin_members = []

    try:
        board = Board.objects.get(project=project)
    except:
        board = Board(project=project)
        
    for i in admin_users:
        admin_members.append(members.get(user=i))

    addMemberform = AddMemberForm(request.POST)
    
    if request.POST and addMemberform.is_valid:
        new_member = addMemberform.data['project_member']
        try:
            new_member_user = User.objects.get(username=new_member)
            member = Project_Member.objects.get(user=new_member_user)
            project.project_members.add(member)
        except:
            messages.info(request,'Invalid user') 
            addMemberform = AddMemberForm()
    else:
        addMemberform = AddMemberForm()

    #add board to the main project page
    # Adding Todo to the main page
    todo = Todo.objects.filter(project=project).order_by('rank')
    paginator = Paginator(todo, 3)  #Creating multiples QuerySet object with defined number in each list
    page = request.GET.get('page') #Get the page parameter of the request object
    page_todo = paginator.get_page(page) #Chossing the correct list with correct 'page' parameter

    #Add event object
    event = Event.objects.filter(project=project).filter(start_time__gte = datetime.now()).order_by('start_time')
    if 'order' in request.GET:        
        order = request.GET['order']
        if order != 'None':
            if order == 'start':
                event = event.order_by('start_time')
            else:
                event = event.order_by('end_time')

    paginator = Paginator(event,3)
    page = request.GET.get('page')
    page_event = paginator.get_page(page)

    #Add thread object
    thread = Thread.objects.filter(project=project).order_by('-last_posted')
    paginator = Paginator(thread,3)
    page = request.GET.get('page')
    page_thread = paginator.get_page(page)

    context = {
        'project':project, 
        'members':members, 
        'admin_members':admin_members, 
        'addMemberform':addMemberform, 
        'admin_users':admin_users, 
        'board':board,
        'todo': page_todo,
        'event': page_event,
        'thread': page_thread,
        'previous_options': request.GET,
        'Year': datetime.now().strftime("%Y")
    }
    
    return render(request, 'project/home.html', context)

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

    context = {
        'project':project, 
        'member':member, 
        'deleteform': deleteform,
        'Year': datetime.now().strftime("%Y")
    }
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

    context = {
        'project':project, 
        'deleteform': deleteform,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'project/delete_project.html', context)


@login_required
@user_is_project_member
def leaveProject(request, pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    admin = project.project_admin.all()
    #Count number of admin
    no_of_admins = len(admin)

    user_member = members.get(user=request.user)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        if no_of_admins == 1 and request.user in admin:
            print(no_of_admins)
            messages.info(request,  'Error: Project must have at least 1 project admin!')
        else:
            if request.user in admin:
                project.project_admin.remove(request.user)
                project.project_members.remove(user_member)
                return redirect('/')
            else:
                project.project_members.remove(user_member)
                return redirect('/')
    else:
        deleteform = DeleteForm()

    context = {
        'project':project,
        'user_member':user_member,
        'deleteform': deleteform,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'project/leave_project.html', context)


@login_required
@user_is_project_member
@user_is_project_admin
def setAdmin(request, pk, member_pk):
    project = Project.objects.get(id=pk)
    member = project.project_members.get(id=member_pk)
    user = User.objects.get(project_member=member)
    setadminform = SetAdminForm(request.POST)
    if request.method == 'POST' and setadminform.data:
        project.project_admin.add(user)
        return redirect('/project/' + str(pk) + '/')
    else:
        setadminform = SetAdminForm()

    context = {
        'project':project, 
        'member':member, 
        'setadminform': setadminform, 
        'user':user,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'project/set_admin.html', context)


@login_required
@user_is_project_member
@user_is_project_admin
def removeAdmin(request, pk, member_pk):
    project = Project.objects.get(id=pk)
    member = project.project_members.get(id=member_pk)
    user = User.objects.get(project_member=member)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        project.project_admin.remove(user)
        return redirect('/project/' + str(pk) + '/')
    else:
        deleteform = DeleteForm()

    context = {
        'project':project, 
        'member':member, 
        'deleteform': deleteform, 
        'user':user,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'project/remove_admin.html', context)
