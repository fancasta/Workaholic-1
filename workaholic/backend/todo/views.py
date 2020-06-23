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
from cal.models import Event
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
        todoform = TodoForm(pk, request.POST)
        added_by = members.get(user=request.user)
        new_todo_title = todoform.data['title']
        new_todo_desc = todoform.data['description']
        deadline = todoform.data['deadline']
        assigned_to = members.get(pk=todoform.data['assigned_to'])
        new_todo = Todo(title=new_todo_title, description=new_todo_desc, last_modified_by=added_by, project=project, rank=last_rank+1, last_modified=datetime.now(), deadline=deadline, assigned_to=assigned_to)
        new_todo.save()

        new_event = Event(project=project, todo=new_todo, title=new_todo_title, description=new_todo_desc, start_time = None,end_time=deadline, label='Todo')
        new_event.save()
        project.todo_set.add(new_todo)

        modified_by = members.get(user=request.user)
        project.cal_last_modified = datetime.now()
        project.cal_last_modified_by = modified_by
        project.last_modified = datetime.now()
        project.last_modified_by = modified_by
        project.save()

        return redirect('/project/' + str(pk) + '/todo')
    else:
        todoform = TodoForm(pk)

    context = {
        'project':project, 
        'members':members, 
        'todoform':todoform, 
        'todo':todo,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'todo/todo_page.html', context)

@login_required
@user_is_project_member
def deleteTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()

    todo = project.todo_set.get(id=todo_pk)
    remaining_todo_set = Todo.objects.filter(project=project)
    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:

        for i in remaining_todo_set:
            if i.rank > todo.rank:
                i.rank -=1
                i.save()
        event = Event.objects.get(todo=todo)
        event.delete()
        todo.delete()

        modified_by = members.get(user=request.user)
        project.cal_last_modified = datetime.now()
        project.cal_last_modified_by = modified_by
        project.last_modified = datetime.now()
        project.last_modified_by = modified_by
        project.save()

        return redirect('/project/' + str(pk) + '/todo/')
    else:
        deleteform = DeleteForm()

    context = {
        'project':project, 
        'todo':todo, 
        'deleteform': deleteform,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'todo/delete_todo.html', context)


@login_required
@user_is_project_member
def upTodoRank(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    remaining_todo_set = Todo.objects.filter(project=project)
    if request.method=="GET":
        if todo.rank == 1:
            return redirect('/project/' + str(pk) + '/todo/')
        for i in remaining_todo_set:
            if todo.rank-i.rank == 1:
                i.rank +=1
                i.save()
        todo.rank -=1 
        todo.save()
        return redirect('/project/' + str(pk) + '/todo/')
    context = {
        'project':project, 
        'todo':todo,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'todo/todo_page.html', context)


@login_required
@user_is_project_member
def downTodoRank(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    remaining_todo_set = Todo.objects.filter(project=project)
    max_rank = remaining_todo_set.order_by('-rank')[0].rank
    if request.method=="GET":
        if todo.rank == max_rank:
            return redirect('/project/' + str(pk) + '/todo/')
        for i in remaining_todo_set:
            if i.rank-todo.rank == 1:
                i.rank -=1
                i.save()
        todo.rank +=1 
        todo.save()
        return redirect('/project/' + str(pk) + '/todo/')
    context = {
        'project':project, 
        'todo':todo,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'todo/todo_page.html', context)


@login_required
@user_is_project_member
def editTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    members = project.project_members.all()

    if request.method == 'POST':
        editForm = TodoForm(pk, request.POST)
        modified_by = members.get(user=request.user)
        todo.title = editForm.data['title']
        todo.description = editForm.data['description']
        todo.deadline = editForm.data['deadline']
        todo.assigned_to = members.get(pk=editForm.data['assigned_to'])

        todo.last_modified_by = modified_by
        todo.last_modified = datetime.now()
        todo.save()

        event = Event.objects.get(todo=todo)
        event.title = todo.title
        event.desc = todo.description
        event.end_time = todo.deadline
        event.save()

        project.cal_last_modified = datetime.now()
        project.cal_last_modified_by = modified_by
        project.last_modified = datetime.now()
        project.last_modified_by = modified_by
        project.save()
        return redirect('/project/' + str(pk) + '/todo/')
    else:
        editForm = TodoForm(pk, instance=todo)

    context = {
        'project':project, 
        'todo':todo, 
        'editform': editForm,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'todo/edit_todo.html', context)
