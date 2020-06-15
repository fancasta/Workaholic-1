from django.db import models
from django.contrib.auth.models import User
from accounts.models import *


# Create your models here.

class Todo(models.Model):
    todo = models.TextField(null=True)
    rank = models.PositiveSmallIntegerField(null=True)
    last_modified_by = models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name='todo_last_modified')
    assigned_to = models.ForeignKey(Project_Member, on_delete=models.CASCADE, null=True, related_name='todo_assigned_to')

    last_modified = models.DateTimeField()
    deadline = models.DateTimeField(null=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

