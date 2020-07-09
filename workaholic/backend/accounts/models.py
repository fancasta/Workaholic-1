from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project_Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Project(models.Model):
    name = models.CharField(max_length=20)
    project_admin = models.ManyToManyField(User)
    project_members = models.ManyToManyField(Project_Member)
    
    calendar_month = models.DateTimeField()
    cal_last_modified_by = models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name='cal_last_modified',null=True)
    cal_last_modified = models.DateTimeField(null=True)

    board_last_modified_by =  models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name='board_last_modified',null=True)
    board_last_modified = models.DateTimeField(null=True)

    forum_last_modified_by =  models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name='forum_last_modified',null=True)
    forum_last_modified = models.DateTimeField(null=True)

    last_modified_by = models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name='project_last_modified', null=True)
    last_modified = models.DateTimeField(null=True)
    last_modified_item = models.CharField(null=True, max_length=20)

    def __str__(self):
        return self.name

