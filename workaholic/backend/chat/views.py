from django.shortcuts import render

from project.decorators import user_is_project_member
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
@user_is_project_member
def index(request, pk):
    context = {'pk':pk}
    return render(request, 'chat/index.html',context)
