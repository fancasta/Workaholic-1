from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from accounts.models import *
from .forms import *
from project.decorators import user_is_project_member, user_is_project_admin

# Create your views here.

@login_required
@user_is_project_member
def todoPage(request,pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    todo = Todo.objects.filter(project=project).order_by('rank')
    if len(todo) > 0:
        last_rank = todo.last().rank
    else:
        last_rank = 0

    if request.method == "POST":
        todoform = TodoForm(request.POST)
        added_by = members.get(user=request.user)
        new_todo_text = todoform.data['todo']
        new_todo = Todo(todo=new_todo_text, last_modified_by=added_by ,project=project, rank=last_rank+1, last_modified=datetime.now())
        new_todo.save()
        project.todo_set.add(new_todo)
        return redirect('/project/' + str(pk) + '/todo')
    else:
        todoform = TodoForm()

    context = {'project':project, 'members':members, 'todoform':todoform, 'todo':todo}
    return render(request, 'todo/todo_page.html', context)

@login_required
@user_is_project_member
@user_is_project_admin
def deleteTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    remaining_todo_set = Todo.objects.filter(project=project)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        for i in remaining_todo_set:
            if i.rank > todo.rank:
                i.rank -=1
                i.save()
        todo.delete()
        return redirect('/project/' + str(pk) + '/todo/')
    else:
        deleteform = DeleteForm()

    context = {'project':project, 'todo':todo, 'deleteform': deleteform}
    return render(request, 'todo/delete_todo.html', context)


@login_required
@user_is_project_member
def upTodoRank(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    remaining_todo_set = Todo.objects.filter(project=project)
    if request.method=="GET":
        for i in remaining_todo_set:
            if todo.rank-i.rank == 1:
                i.rank +=1
                i.save()
        todo.rank -=1 
        todo.save()
        return redirect('/project/' + str(pk) + '/todo/')
    context = {'project':project, 'todo':todo}
    return render(request, 'todo/todo_page.html', context)


@login_required
@user_is_project_member
def downTodoRank(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    remaining_todo_set = Todo.objects.filter(project=project)
    if request.method=="GET":
        for i in remaining_todo_set:
            if i.rank-todo.rank == 1:
                i.rank -=1
                i.save()
        todo.rank +=1 
        todo.save()
        return redirect('/project/' + str(pk) + '/todo/')
    context = {'project':project, 'todo':todo}
    return render(request, 'todo/todo_page.html', context)


@login_required
@user_is_project_member
def editTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    members = project.project_members.all()
    editForm = EditTodoForm(request.POST)
    if request.method == 'POST' and todo.todo != editForm.data:
        modified_by = members.get(user=request.user)
        todo.todo = editForm.data['todo']
        todo.last_modified_by = modified_by
        todo.last_modified = datetime.now()
        todo.save()
    else:
        editForm = EditTodoForm()

    context = {'project':project, 'todo':todo, 'editForm': editForm}
    return render(request, 'todo/edit_todo.html', context)
