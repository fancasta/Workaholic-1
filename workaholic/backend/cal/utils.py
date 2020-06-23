from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
from accounts.models import *

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, action=None):
        self.year = year
        self.month = month
        self.action = action
        super().__init__()
    
    def formatday(self, pk, day, start_events, end_events):
        d = ''
        if start_events:
            events_start_per_day = start_events.filter(start_time__day=day)                
            for event in events_start_per_day:
                d += f'<li> Start day: {event.view_event_url} <kbd>{event.label}</kbd> </li>'
        
        events_end_per_day = end_events.filter(end_time__day=day)
        for event in events_end_per_day:
            d += f'<li> End day: {event.view_event_url} <kbd>{event.label}</kbd> </li>'
    
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return f'<td></td>'

    def formatweek(self, pk, theweek, start_events, end_events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(pk, d, start_events, end_events)
        return f'<tr>{week}</tr>'

    def formatmonth(self, pk, withyear=True):
        project = Project.objects.get(id=pk)
        start_events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, project=project)
        end_events = Event.objects.filter(end_time__year=self.year, end_time__month=self.month, project=project)
        cal = f'<table border="10" cellpadding="10" cellspacing="10" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(pk, week, start_events, end_events)}\n'
        return cal