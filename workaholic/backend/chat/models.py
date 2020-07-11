from django.db import models

from accounts.models import Project, Project_Member
from datetime import datetime
# Create your models here.

class Message(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    sender = models.ForeignKey(Project_Member, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now=True)
