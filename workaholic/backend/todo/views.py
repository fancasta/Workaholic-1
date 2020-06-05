from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import *
from .forms import *
from project.decorators import user_is_project_member, user_is_project_admin

# Create your views here.

@login_required
@user_is_project_member
def todoPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    if request.method == "POST":
        todoform = TodoForm(request.POST)
        added_by = members.get(user=request.user)
        new_todo_text = todoform.data['todo']
        new_todo = Todo(todo=new_todo_text, added_by=added_by ,project=project)
        new_todo.save()
        project.todo_set.add(new_todo)
        return redirect('/project/' + str(pk) + '/todo')
    else:
        todoform = TodoForm()

    todo = Todo.objects.filter(project=project)
    admin_member = members.get(user=project.project_admin)

    context = {'project':project, 'members':members, 'todoform':todoform, 'todo':todo, 'admin_member':admin_member}
    return render(request, 'todo/todo_page.html', context)

@login_required
@user_is_project_member
@user_is_project_admin
def deleteTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        todo.delete()
        return redirect('/project/' + str(pk) + '/')
    else:
        deleteform = DeleteForm()

    context = {'project':project, 'todo':todo, 'deleteform': deleteform}
    return render(request, 'todo/delete_todo.html', context)

@login_required
@user_is_project_member
def editTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    editForm = EditTodoForm(request.POST)
    if request.method == 'POST' and todo.todo != editForm.data:
        todo.todo = editForm.data['todo']
        todo.save()
    else:
        editForm = EditTodoForm()

    context = {'project':project, 'todo':todo, 'editForm': editForm}
    return render(request, 'todo/edit_todo.html', context)
