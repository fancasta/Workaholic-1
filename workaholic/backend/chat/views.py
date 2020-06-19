from django.shortcuts import render

from project.decorators import user_is_project_member
from django.contrib.auth.decorators import login_required
from accounts.models import *
from datetime import datetime
# Create your views here.

@login_required
@user_is_project_member
def index(request, pk):
    project = Project.objects.get(id=pk)

    context = {
        'pk':pk,
        'project':project,
        'Year': datetime.now().strftime("%Y")
    }

    return render(request, 'chat/index.html',context)
