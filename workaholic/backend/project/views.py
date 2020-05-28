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

from .decorators import user_is_project_member
from .forms import *
from .models import Todo

# Create your views here.

@login_required
@user_is_project_member
def projectPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    if request.method == "POST":
        todoform = TodoForm(request.POST)
        added_by = members.get(user=request.user)
        new_todo_text = todoform.data['todo']
        new_todo = Todo(todo=new_todo_text, added_by=added_by ,project=project)
        new_todo.save()
        project.todo_set.add(new_todo)
        return redirect('/project/' + str(pk) + '/')
    else:
        todoform = TodoForm()

    todo = Todo.objects.filter(project=project)

    context = {'project':project, 'members':members, 'todoform':todoform, 'todo':todo}
    return render(request, 'project/home.html', context)

@login_required
@user_is_project_member
def deleteTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    deleteform = DeleteTodoForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        todo.delete()
        return redirect('/project/' + str(pk) + '/')
    else:
        deleteform = DeleteTodoForm()

    context = {'project':project, 'todo':todo, 'deleteform': deleteform}
    return render(request, 'project/delete_todo.html', context)

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
