from django.db import models

# Create your models here.
from accounts.models import *

# Create your models here.

class Thread(models.Model):
    title = models.CharField(max_length=60, null=True)
    created_by = models.ForeignKey(Project_Member, related_name="thread_creater",on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, related_name="project_thread",on_delete=models.CASCADE)
    last_posted = models.DateTimeField(null=True)
    last_posted_by = models.ForeignKey(Project_Member, related_name="last_posted_by",on_delete=models.CASCADE, null=True)

class Post(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField()
    project = models.ForeignKey(Project, related_name="project_post",on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, related_name="thread_post",on_delete=models.CASCADE)
    posted_by = models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name="post_sender", null=True, default=None)

    quote_content = models.TextField(null=True, default=None)
    quote_sender = models.ForeignKey(Project_Member, on_delete=models.CASCADE, related_name="quote_sender", null=True, default=None)
    quote_timestamp = models.DateTimeField(null=True, default=None)

    edited = models.BooleanField(default=False)

