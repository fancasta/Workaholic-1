from django.db import models
from accounts.models import Project
from django.urls import reverse
from todo.models import Todo
from datetime import datetime

# Create your models here.

class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    
    start_time = models.DateTimeField(null=True, blank=True, default= datetime.now)
    start_month = models.IntegerField(null=True)
    start_year = models.IntegerField(null=True)

    end_time = models.DateTimeField(null=True, blank=True, default=None)
    end_month = models.IntegerField(null=True)
    end_year = models.IntegerField(null=True)

    label = models.CharField(max_length=20, null=True, blank=True)
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=True, blank=True)
    
    @property
    def view_event_url(self):
        url = 'event/' + str(self.id) + '/'
        for i in self.title.split():
            if len(i) > 10:
                return f'<a href="{url}"> {self.title[:8] + "..."} </a>'

        return f'<a href="{url}"> {self.title} </a>'
        

    @property
    def edit_event_url(self):
        url = 'event/' + str(self.id) + '/' + 'edit_event/'
        return f'<a href="{url}"> Edit </a>'

    @property
    def delete_event_url(self):
        url = 'event/' + str(self.id) + '/delete_event/'
        return f'<a href="{url}"> Delete </a>'