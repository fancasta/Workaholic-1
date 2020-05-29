from django.db import models
from django.contrib.auth.models import User
from accounts.models import *

# Create your models here.

class Todo(models.Model):
    todo = models.CharField(max_length=50, null=True)
    added_by = models.ForeignKey(Project_Member, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
