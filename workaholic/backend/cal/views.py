from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .options import label_options, month_options
from django.core.paginator import Paginator #import Paginator

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

    current_month_tag = datetime.now().date().strftime('%B %Y ')
    prev_month_tag = datetime(get_date(prev_month(d)).year, get_date(prev_month(d)).month, 1).strftime('%B %Y ')
    next_month_tag = datetime(get_date(next_month(d)).year, get_date(next_month(d)).month, 1).strftime('%B %Y ')

    context = {
        'project':project, 
        'calendar':html_cal,
        'label_options':label_options,
        'month_options':month_options,
        'current_month_tag': current_month_tag,
        'prev_month_tag': prev_month_tag,
        'next_month_tag': next_month_tag,
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
    modified_by = members.get(user=request.user)

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
            start_date = datetime.strptime(form.data['start_time'], '%Y-%m-%dT%H:%M')
            event.start_month = start_date.strftime("%m")
            event.start_year = start_date.strftime("%Y")

            event.end_month = 0
            event.end_year = 0

            event.save()
        else:
            event.start_time = form.data['start_time']
            start_date = datetime.strptime(form.data['start_time'], '%Y-%m-%dT%H:%M')
            event.start_month = start_date.strftime("%m")
            event.start_year = start_date.strftime("%Y")

            event.end_time = form.data['end_time']
            end_date = datetime.strptime(form.data['end_time'], '%Y-%m-%dT%H:%M')
            event.end_month = end_date.strftime("%m")
            event.end_year = end_date.strftime("%Y")

            event.save()

        try:
            todo = Todo.objects.get(event=event)
            todo.deadline = event.end_time
            todo.title = event.title
            todo.description = event.description
            todo.last_modified = datetime.now()
            todo.last_modified_by = modified_by
            todo.save()
            
        except:
            event.label = form.data['label']
            event.save()
        
        project.cal_last_modified = datetime.now()
        project.cal_last_modified_by = modified_by
        project.last_modified = datetime.now()
        project.last_modified_by = modified_by
        project.last_modified_item = "Todo"
        project.save()
        
        return redirect('/project/' + str(pk) + '/calendar/')
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

@login_required
@user_is_project_member
def searchEvent(request, pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    events = Event.objects.filter(project=project)
    searched_events = events

    #Take input from the calendar.html
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            searched_events = searched_events.filter(title__icontains=keywords)
            
    if 'label' in request.GET:        
        label = request.GET['label']
        if label != 'None':
            searched_events = searched_events.filter(label=label)
    if 'start_month' in request.GET:        
        start_month = request.GET['start_month']
        start_month = int(start_month) #When you try to pass 0 in the url and try to get the parameter, you will receive empty or null.
        # When you take a parameter from the url, you will always receive a string, not an integer. So you have to change to interger before you can do any kind of comparison
        if start_month != 0: 
            searched_events = searched_events.filter(start_month=start_month)

    if 'start_year' in request.GET:        
        start_year = request.GET['start_year']
        if start_year:
            start_year = int(start_year)
            searched_events = searched_events.filter(start_year=start_year)

    if 'end_month' in request.GET:        
        end_month = request.GET['end_month']
        end_month = int(end_month)
        if end_month != 0:
            searched_events = searched_events.filter(end_month=end_month)
            
    if 'end_year' in request.GET:        
        end_year = request.GET['end_year']
        if end_year:
            end_year = int(end_year)
            searched_events = searched_events.filter(end_year=end_year)

    paginator = Paginator(searched_events,6)
    page = request.GET.get('page')
    page_events = paginator.get_page(page)

    context = {
        'project':project, 
        'events':page_events,
        'members':members,
        'label_options':label_options,
        'month_options':month_options,
        'previous_options': request.GET, 
        'Year': datetime.now().strftime("%Y")
    }

    return render(request, 'cal/search_event.html', context)