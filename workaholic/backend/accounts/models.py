from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project_Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=20)
    project_members = models.ManyToManyField(Project_Member)

    def __str__(self):
        return self.name
