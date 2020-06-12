from django.db import models
from accounts.models import Project
from django.urls import reverse

# Create your models here.

class Event(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = 'event/' + str(self.id) + '/'
        return f'<a href="{url}"> {self.title} </a>'

