from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Project_Member)
admin.site.register(Project)


