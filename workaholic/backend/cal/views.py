from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required

from django.urls import reverse

# Create your views here.

import calendar

from accounts.models import *
from project.decorators import *

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
        return redirect('/project/' + str(pk) + '/calendar/')
    elif action == 'prev_month':
        d = get_date(prev_month(d))
        project.calendar_month = d
        project.save()
        return redirect('/project/' + str(pk) + '/calendar/')
    elif action == 'next_month':
        d = get_date(next_month(d))
        project.calendar_month = d
        project.save()
        return redirect('/project/' + str(pk) + '/calendar/')


    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(pk, withyear=True)
    context = {'project':project, 'calendar':html_cal}
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
def event(request, pk, event_id=None):
    project = Project.objects.get(id=pk)
    if event_id:
        event = Event.objects.filter(project=project).get(id=event_id)
    else:
        event = Event(project=project, start_time=datetime.now(), end_time=(datetime.now() + timedelta(weeks=1)))
    
    if request.POST:
        form = EventForm(request.POST)
        event.title = form.data['title']
        event.description = form.data['description']
        event.start_time = form.data['start_time']
        event.end_time = form.data['end_time']
        event.save()
        return redirect('/project/' + str(pk) + '/calendar/')
    else:
        form = EventForm(instance=event)

    context = {'project':project,'form': form, 'event':event}
    return render(request, 'cal/event.html', context)

