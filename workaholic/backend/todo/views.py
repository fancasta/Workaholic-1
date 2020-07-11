from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator #import Paginator

from accounts.models import *
from cal.models import Event
from .forms import *
from project.decorators import user_is_project_member, user_is_project_admin
from .options import rank_options, month_options

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
        end_date = datetime.strptime(deadline, '%Y-%m-%dT%H:%M')
        deadline_month = end_date.strftime("%m")
        deadline_year = end_date.strftime("%Y")

        assigned_to = members.get(pk=todoform.data['assigned_to'])
        new_todo = Todo(title=new_todo_title, description=new_todo_desc, last_modified_by=added_by, project=project, rank=last_rank+1, last_modified=datetime.now(), deadline=deadline,deadline_month=deadline_month, deadline_year=deadline_year, assigned_to=assigned_to)
        new_todo.save()

        new_event = Event(project=project, todo=new_todo, title=new_todo_title, description=new_todo_desc, start_time = None,start_month=0,start_year=0,end_time=deadline,end_month=end_date.strftime("%m"),end_year=end_date.strftime("%Y"), label='Todo')
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
        'rank_options': rank_options,
        'month_options': month_options,
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
            return redirect('/project/' + str(pk) + '/todo/' +'#todo')
        for i in remaining_todo_set:
            if todo.rank-i.rank == 1:
                i.rank +=1
                i.save()
        todo.rank -=1 
        todo.save()
        return redirect('/project/' + str(pk) + '/todo/' +'#todo')
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
            return redirect('/project/' + str(pk) + '/todo/' +'#todo')
        for i in remaining_todo_set:
            if i.rank-todo.rank == 1:
                i.rank -=1
                i.save()
        todo.rank +=1 
        todo.save()
        return redirect('/project/' + str(pk) + '/todo/' +'#todo')
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
        end_date = datetime.strptime(todo.deadline, '%Y-%m-%dT%H:%M')
        todo.deadline_month = end_date.strftime("%m")
        todo.deadline_year = end_date.strftime("%Y")

        todo.assigned_to = members.get(pk=editForm.data['assigned_to'])

        todo.last_modified_by = modified_by
        todo.last_modified = datetime.now()
        todo.save()

        event = Event.objects.get(todo=todo)
        event.title = todo.title
        event.description = todo.description
        event.start_month = 0
        event.start_year = 0

        event.end_time = todo.deadline
        event.end_month = end_date.strftime("%m")
        event.end_year = end_date.strftime("%Y")

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

@login_required
@user_is_project_member
def viewTodo(request, pk, todo_pk):
    project = Project.objects.get(id=pk)
    todo = project.todo_set.get(id=todo_pk)
    members = project.project_members.all()

    context = {
        'project':project, 
        'todo': todo,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'todo/view_todo.html', context)

@login_required
@user_is_project_member
def searchTodo(request, pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    todos = Todo.objects.filter(project=project).order_by('rank')
    searched_todos = todos

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            searched_todos = searched_todos.filter(description__icontains=keywords)|searched_todos.filter(title__icontains=keywords)
    
    if 'assigned_to' in request.GET:        
        assigned_to = request.GET['assigned_to']
        if assigned_to != 'None':
            searched_todos = searched_todos.filter(assigned_to=assigned_to)
    
    if 'deadline_month' in request.GET:        
        deadline_month = request.GET['deadline_month']
        deadline_month = int(deadline_month)
        if deadline_month != 0:
            searched_todos = searched_todos.filter(deadline_month=deadline_month)

    if 'deadline_year' in request.GET:        
        deadline_year = request.GET['deadline_year']
        if deadline_year:
            deadline_year = int(deadline_year)
            searched_todos = searched_todos.filter(deadline_year=deadline_year)

    if 'rank' in request.GET:        
        rank = request.GET['rank']
        rank = int(rank)
        if rank != 0:
            count = 1
            new_searched_todos = []
            for i in searched_todos:
                if count <= rank:
                    new_searched_todos.append(i)
                    count += 1
                else:
                    break
            searched_todos = new_searched_todos

    paginator = Paginator(searched_todos,6)
    page = request.GET.get('page')
    page_todos = paginator.get_page(page)

    context = {
        'project':project, 
        'members': members,
        'todos': page_todos,
        'rank_options': rank_options,
        'month_options': month_options,
        'previous_options': request.GET, 
        'Year': datetime.now().strftime("%Y")
    }

    return render(request, 'todo/search_todo.html', context)