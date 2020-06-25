from django.db import models
from django.contrib.auth.models import User
from accounts.models import *
from datetime import datetime

# Create your models here.

class Todo(models.Model):
    title = models.CharField(null=True, max_length=30)
    description = models.TextField(null=True, blank=True)

    rank = models.PositiveSmallIntegerField()
    last_modified_by = models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name='todo_last_modified')
    assigned_to = models.ForeignKey(Project_Member,default= Project_Member, on_delete=models.CASCADE, null=True, related_name='todo_assigned_to')

    last_modified = models.DateTimeField()
    deadline = models.DateTimeField(null=True, default= datetime.now)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

