from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

from accounts.models import Project

# Create your models here.

class Board(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    body = RichTextUploadingField(blank=True, null=True)

