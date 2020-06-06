from django.shortcuts import render, redirect 
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.models import *
from project.decorators import user_is_project_member, user_is_project_admin

from .models import Board
from .forms import BoardForm


@login_required
@user_is_project_member
def boardPage(request, pk):
    project = Project.objects.get(id=pk)
    board_list = Board.objects.filter(project=project)
    if len(board_list)==0:
            board = Board(project=project)
            board.save()
    else:
        board = board_list[0]
    if request.method == 'POST':
        form = BoardForm(request.POST)
        board.body = form.data['body']
        board.save()
        return redirect('/project/' + str(pk) + '/board/')
    else:
        form = BoardForm(instance=board)
    context = {'project':project, 'form':form, 'board':board}
    return render(request, 'board/board_page.html', context)
