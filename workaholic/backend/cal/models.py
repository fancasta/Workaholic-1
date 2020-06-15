from django.db import models
from accounts.models import Project
from django.urls import reverse

from todo.models import Todo

# Create your models here.

class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, null=True)
    
    @property
    def get_html_url(self):
        url = 'event/' + str(self.id) + '/'
        return f'<a href="{url}"> {self.title} </a>'

