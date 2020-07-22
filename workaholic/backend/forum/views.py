from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
# Create your views here.
from django import forms
from django.contrib.auth.models import User
from django.core.paginator import Paginator #import Paginator

from accounts.models import *
from project.decorators import *
from .decorators import user_is_post_creater_or_project_admin, user_is_thread_creater_or_project_admin, user_is_post_creater

from .forms import *
from .models import *

@login_required
@user_is_project_member
def forumPage(request, pk):
    project = Project.objects.get(id=pk)
    thread = Thread.objects.filter(project=project).order_by('-last_posted')
    members = project.project_members.all()
    project_admin = project.project_admin.all()
    user_member = members.get(user=request.user)

    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            thread = thread.filter(title__icontains=keywords)
    
    if 'date' in request.GET:        
        date = request.GET['date']
        if date != 'None':
            if date == 'new':
                thread = thread.order_by('-last_posted')
            else:
                thread = thread.order_by('last_posted')

    if request.method == "POST":
        threadform = ThreadForm(request.POST)
        thread_title = threadform.data['title']
        new_thread = Thread(created_by=user_member, title=thread_title, project=project)
        new_thread.save()

        postform = PostForm(request.POST)
        post_content = postform.data['content']
        new_post = Post(posted_by=user_member, thread=new_thread, content=post_content, project=project, timestamp=datetime.now())
        new_post.save()
        new_thread.last_posted = datetime.now()
        new_thread.last_posted_by = user_member
        new_thread.save()

        project.forum_last_modified = datetime.now()
        project.forum_last_modified_by = user_member
        project.last_modified = datetime.now()
        project.last_modified_by = user_member
        project.last_modified_item = "Forum"
        project.save()

        return redirect('/project/' + pk + '/forum/' + str(new_thread.pk) + '/view_thread/')
    else:
        threadform = ThreadForm()
        postform = PostForm()

    context = {
        'project':project, 
        'members':members, 
        'threadform': threadform, 
        'postform': postform,
        'thread': thread,
        'user_member': user_member,
        'previous_options': request.GET,
        'project_admin': project_admin
    }
    return render(request, 'forum/forum.html', context)



@login_required
@user_is_project_member
def threadPage(request, pk, thread_pk):
    project = Project.objects.get(id=pk)
    thread = Thread.objects.get(pk=thread_pk)
    members = project.project_members.all()
    project_admin = project.project_admin.all()
    user_member = members.get(user=request.user)

    #Load Messages
    posts = Post.objects.filter(project=project, thread=thread).order_by('timestamp')

    first_post = posts.order_by('timestamp')[0]
    id_1st = first_post.id
    posts = posts.exclude(id=id_1st)

    #If I put this thing first then when I say posts = posts.exclude

    if 'order' in request.GET:        
        order = request.GET['order']
        if order != 'None':
            if order == 'popular':
                posts = posts.order_by('-like_counter')
            elif order == 'new':
                posts = posts.order_by('-timestamp')
            else:
                posts = posts.order_by('timestamp')

    if len(posts) == 1:
        thread.last_posted = posts[0].timestamp
        thread.last_posted_by = posts[0].posted_by
        thread.save()

    if request.method == "POST":
        postform = PostForm(request.POST)
        post_content = postform.data['content']
        new_post = Post(posted_by=user_member, thread=thread, content=post_content, project=project, timestamp=datetime.now())
        new_post.save()
        thread.last_posted = datetime.now()
        thread.last_posted_by = user_member
        thread.save()

        #Local paginator after create a new post
        posts = Post.objects.filter(project=project, thread=thread).order_by('timestamp')
        first_post = posts.order_by('timestamp')[0]
        id_1st = first_post.id
        posts = posts.exclude(id=id_1st)
        paginator = Paginator(posts,6)
        page = request.GET.get('page')
        page_posts = paginator.get_page(page)

        project.forum_last_modified = datetime.now()
        project.forum_last_modified_by = user_member
        project.last_modified = datetime.now()
        project.last_modified_by = user_member
        project.last_modified_item = "Forum"
        project.save()

        return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/' + '?page=' + str(paginator.num_pages) + '#pagination')
    else:
        postform = PostForm()

    paginator = Paginator(posts,6)
    page = request.GET.get('page')
    page_posts = paginator.get_page(page)

    #Change the liked field based on the user
    for i in page_posts: 
        if i.like.filter(id=user_member.id).exists():
            i.liked = True

    context = {
        'project':project, 
        'members':members, 
        'user_member': user_member,
        'postform': postform, 
        'posts': page_posts,
        'thread': thread,
        'first_post': first_post,
        'previous_options': request.GET,
        'project_admin': project_admin
    }
    return render(request, 'forum/thread.html', context)



#Change to Post
@login_required
@user_is_project_member
@user_is_thread_creater_or_project_admin
def deleteThread(request, pk, thread_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)

    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        thread.delete()

        return redirect('/project/' + pk + '/forum/')
    else:
        deleteform = DeleteForm()

    context = {
        'project':project, 
        'members':members, 
        'deleteform': deleteform,
        'thread':thread
    }
    return render(request, 'forum/delete_thread.html', context)

#Change to Post
@login_required
@user_is_project_member
@user_is_thread_creater_or_project_admin
def editThread(request, pk, thread_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)

    if request.method == 'POST':
        threadform = ThreadForm(request.POST, instance=thread)
        thread.title = threadform.data['title']
        thread.save()

        return redirect('/project/' + pk + '/forum/')
    else:
        threadform = ThreadForm(instance=thread)

    context = {
        'project':project, 
        'members':members, 
        'threadform': threadform, 
        'thread':thread
    }
    return render(request, 'forum/edit_thread.html', context)

#Change to Post
@login_required
@user_is_project_member
@user_is_post_creater_or_project_admin
def deletePost(request, pk, thread_pk, post_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)
    post = Post.objects.get(id=post_pk)

    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        post.delete()

        return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/')
    else:
        deleteform = DeleteForm()

    context = {
        'project':project, 
        'members':members, 
        'deleteform': deleteform,
        'post': post,
        'thread':thread
    }
    return render(request, 'forum/delete_post.html', context)


#Change to Post
@login_required
@user_is_project_member
@user_is_post_creater
def editPost(request, pk, thread_pk, post_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)
    thread = Thread.objects.get(pk=thread_pk)
    post = Post.objects.get(id=post_pk)

    if request.method == "POST":
        postform = PostForm(request.POST, instance=post)
        post_content = postform.data['content']
        post.content = post_content
        post.edited = True
        post.save()

        return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/')
    else:
        postform = PostForm(instance=post)

    context = {
        'project':project, 
        'members':members, 
        'postform': postform, 
        'post': post,
        'thread':thread,
    }
    return render(request, 'forum/edit_post.html', context)


@login_required
@user_is_project_member
def quotePost(request, pk, thread_pk, post_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    project_admin = project.project_admin.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)
    quoted_post = Post.objects.get(id=post_pk)
    quote_content = quoted_post.content
    quote_sender = quoted_post.posted_by
    quote_timestamp = quoted_post.timestamp

    posts = Post.objects.filter(project=project, thread=thread).order_by('-timestamp')
    first_post = posts.order_by('timestamp')[0]
    id_1st = first_post.id
    posts = posts.exclude(id=id_1st)

    if len(posts) == 1:
        thread.last_posted = posts[0].timestamp
        thread.last_posted_by = posts[0].posted_by
        thread.save()

    if request.method == "POST":
        postform = PostForm(request.POST)
        post_content = postform.data['content']
        new_post = Post(posted_by=user_member, thread=thread, content=post_content, project=project, quote_content=quote_content, quote_sender=quote_sender, quote_timestamp=quote_timestamp, timestamp=datetime.now())
        new_post.save()
        thread.last_posted = datetime.now()
        thread.last_posted_by = user_member
        thread.save()

        project.forum_last_modified = datetime.now()
        project.forum_last_modified_by = user_member
        project.last_modified = datetime.now()
        project.last_modified_by = user_member
        project.last_modified_item = "Forum"
        project.save()

        return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/' +'#form')

    else:
        postform = PostForm()

    paginator = Paginator(posts,6)
    page = request.GET.get('page')
    page_posts = paginator.get_page(page)

    #Change the liked field based on the user
    for i in page_posts: 
        if i.like.filter(id=user_member.id).exists():
            i.liked = True

    context = {
        'project':project, 
        'members':members, 
        'user_member': user_member,
        'postform': postform, 
        'posts': page_posts,
        'thread': thread,
        'quoted_post':quoted_post,
        'first_post': first_post,
        'previous_options': request.GET,
        'project_admin': project_admin
    }
    return render(request, 'forum/thread.html', context)

@login_required
@user_is_project_member
def likePost(request, pk, thread_pk, post_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    project_admin = project.project_admin.all()
    user_member = members.get(user=request.user) #The current Project_Member object (link to the current User object)

    thread = Thread.objects.get(pk=thread_pk)
    post = Post.objects.get(id=post_pk)
    post.like.add(user_member)
    if post.like_counter < post.like.count():
        post.like_counter += 1
    post.save()

    page = request.GET.get('page')

    return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/' +'?page=' + str(page) + '#' + str(post.id))

@login_required
@user_is_project_member
def dislikePost(request, pk, thread_pk, post_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    project_admin = project.project_admin.all()
    user_member = members.get(user=request.user) #The current Project_Member object (link to the current User object)

    thread = Thread.objects.get(pk=thread_pk)
    post = Post.objects.get(id=post_pk)
    post.like.remove(user_member)
    if post.like_counter > post.like.count():
        post.like_counter -= 1
    post.save()

    page = request.GET.get('page')

    return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/' + '?page=' + str(page) + '#' + str(post.id))
