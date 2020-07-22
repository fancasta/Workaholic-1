from django.http import HttpResponse
from django.shortcuts import redirect

from accounts.models import *
from forum.models import Thread, Post

def user_is_post_creater(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        members = project.project_members.all()
        user_member = Project_Member.objects.get(user= request.user)

        #Getting the post
        post = Post.objects.get(id=kwargs['post_pk'])

        if user_member == post.posted_by:
            return function(request,  *args, **kwargs)
        else:
            return redirect('/project/' + str(kwargs['pk'])  + '/forum/' + str(kwargs['thread_pk']) + '/view_thread/')
    return wrap

def user_is_post_creater_or_project_admin(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        members = project.project_members.all()
        user_member = Project_Member.objects.get(user= request.user)

        #Getting project admin querylist
        project_admin = project.project_admin.all()

        #Getting the post
        post = Post.objects.get(id=kwargs['post_pk'])

        if request.user in project_admin or user_member == post.posted_by:
            return function(request,  *args, **kwargs)
        else:
            return redirect('/project/' + str(kwargs['pk'])  + '/forum/' + str(kwargs['thread_pk']) + '/view_thread/')
    return wrap

def user_is_thread_creater_or_project_admin(function):
    def wrap(request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        members = project.project_members.all()
        user_member = Project_Member.objects.get(user= request.user)

        #Getting project admin querylist
        project_admin = project.project_admin.all()

        #Getting the thread
        thread = Thread.objects.get(pk=kwargs['thread_pk'])

        if request.user in project_admin or user_member == thread.created_by:
            return function(request,  *args, **kwargs)
        else:
            return redirect('/project/' + str(kwargs['pk'])  + '/forum/')
    return wrap