from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

# Create your views here.

import calendar

from accounts.models import *
from project.decorators import *
from todo.forms import DeleteForm
from todo.models import Todo

from .forms import *
from .models import *
from .utils import Calendar

@login_required
@user_is_project_member
def calendarPage(request,pk,action=None):
    project = Project.objects.get(id=pk)
    events = Event.objects.filter(project=project)
    d = project.calendar_month

    if action == 'current_month':
        d = get_date(request.GET.get('month', None))
        project.calendar_month = d
        project.save()
        return redirect('/project/' + str(pk) + '/calendar/' +'#cal')
    elif action == 'prev_month':
        d = get_date(prev_month(d))
        project.calendar_month = d
        project.save()
        return redirect('/project/' + str(pk) + '/calendar/' +'#cal')
    elif action == 'next_month':
        d = get_date(next_month(d))
        project.calendar_month = d
        project.save()
        return redirect('/project/' + str(pk) + '/calendar/' +'#cal')


    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(pk, withyear=True)
    context = {
        'project':project, 
        'calendar':html_cal,
        'Year': datetime.now().strftime("%Y")
        }
    return render(request,'cal/calendar.html',context)

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
@user_is_project_member
def editEvent(request, pk, event_id=None):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    if event_id:
        event = Event.objects.filter(project=project).get(id=event_id)
    else:
        event = Event(project=project)
    
    if request.method == 'POST':
        form = EventForm(request.POST)
        event.title = form.data['title']
        event.description = form.data['description']

        if form.data['start_time'] == '' and form.data['end_time'] == '':
            messages.info(request, 'Please enter a start time or an end time for your event!')
            return redirect('/project/' + str(pk) + '/calendar/event/add_event/')
        elif form.data['start_time'] == '':
            event.end_time = form.data['end_time']
            event.save()
        elif form.data['end_time'] == '':
            event.start_time = form.data['start_time']
            event.save()
        else:
            event.start_time = form.data['start_time']
            event.end_time = form.data['end_time']
            event.save()

        try:
            todo = Todo.objects.get(event=event)
            todo.deadline = event.end_time
            todo.title = event.title
            todo.description = event.description
            todo.save()
            
        except:
            event.label = form.data['label']
            event.save()

        modified_by = members.get(user=request.user)
        
        project.cal_last_modified = datetime.now()
        project.cal_last_modified_by = modified_by
        project.last_modified = datetime.now()
        project.last_modified_by = modified_by
        project.save()
        
        return redirect('/project/' + str(pk) + '/calendar/event/' + str(event.id) +'/')
    else:
        form = EventForm(instance=event)

    context = {
        'project':project,
        'form': form,
        'event':event,
        'event_pk':event_id,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'cal/event.html', context)

@login_required
@user_is_project_member
def viewEvent(request, pk, event_id):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    event = project.event_set.get(id=event_id)

    context = {
        'project':project, 
        'event':event, 
        'event_pk':event_id,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'cal/view_event.html', context)


@login_required
@user_is_project_member
def deleteEvent(request, pk, event_id):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    event = project.event_set.get(id=event_id)
    deleteform = DeleteForm(request.POST)

    if request.method == 'POST' and deleteform.data:
        try:
            todo = Todo.objects.get(event=event)
            remaining_todo_set = Todo.objects.filter(project=project)
            for i in remaining_todo_set:
                if i.rank > todo.rank:
                    i.rank -=1
                    i.save()
            todo.delete()
            event.delete()
        except:
            event.delete()

        modified_by = members.get(user=request.user)
        project.cal_last_modified = datetime.now()
        project.cal_last_modified_by = modified_by
        project.last_modified = datetime.now()
        project.last_modified_by = modified_by
        project.save()

        return redirect('/project/' + str(pk) + '/calendar/')
    else:
        deleteform = DeleteForm()

    context = {
        'project':project, 
        'event':event, 
        'deleteform': deleteform, 
        'event_pk':event_id,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'cal/delete_event.html', context)
