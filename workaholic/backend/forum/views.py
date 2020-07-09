
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# Create your views here.

from accounts.models import *
from project.decorators import *

from .forms import *
from .models import *

@login_required
@user_is_project_member
def forumPage(request, pk):
    project = Project.objects.get(id=pk)
    thread = Thread.objects.filter(project=project).order_by('-last_posted')
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    if request.method == "POST":
        threadform = ThreadForm(request.POST)
        thread_title = threadform.data['title']
        new_thread = Thread(created_by=user_member, title=thread_title, project=project)
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

    context = {
        'project':project, 
        'members':members, 
        'threadform': threadform, 
        'thread': thread,
    }
    return render(request, 'forum/forum.html', context)



@login_required
@user_is_project_member
def threadPage(request, pk, thread_pk):
    project = Project.objects.get(id=pk)
    thread = Thread.objects.get(pk=thread_pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    #Load Messages
    posts = Post.objects.filter(project=project, thread=thread).order_by('-timestamp')
    
    if len(posts) > 1:
        thread.last_posted = posts[0].timestamp
        thread.last_posted_by = user_member
        thread.save()

    if request.method == "POST":
        postform = PostForm(request.POST)
        post_content = postform.data['content']
        new_post = Post(posted_by=user_member, thread=thread, content=post_content, project=project, timestamp=datetime.now())
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

        return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/')
    else:
        postform = PostForm()

    context = {
        'project':project, 
        'members':members, 
        'user_member': user_member,
        'postform': postform, 
        'posts': posts,
        'thread': thread,
    }
    return render(request, 'forum/thread.html', context)



#Change to Post
@login_required
@user_is_project_member
def deleteThread(request, pk, thread_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)

    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        thread.delete()

        project.forum_last_modified = datetime.now()
        project.forum_last_modified_by = user_member
        project.last_modified = datetime.now()
        project.last_modified_by = user_member
        project.last_modified_item = "Forum"
        project.save()

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
def editThread(request, pk, thread_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)

    if request.method == 'POST':
        threadform = ThreadForm(request.POST, instance=thread)
        thread.title = threadform.data['title']
        thread.save()

        project.forum_last_modified = datetime.now()
        project.forum_last_modified_by = user_member
        project.last_modified = datetime.now()
        project.last_modified_by = user_member
        project.last_modified_item = "Forum"
        project.save()

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
def deletePost(request, pk, thread_pk, post_pk):
    project = Project.objects.get(id=pk)
    members = project.project_members.all()
    user_member = members.get(user=request.user)

    thread = Thread.objects.get(pk=thread_pk)
    post = Post.objects.get(id=post_pk)

    deleteform = DeleteForm(request.POST)
    if request.method == 'POST' and deleteform.data:
        post.delete()

        project.forum_last_modified = datetime.now()
        project.forum_last_modified_by = user_member
        project.last_modified = datetime.now()
        project.last_modified_by = user_member
        project.last_modified_item = "Forum"
        project.save()

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
    user_member = members.get(user=request.user)
    thread = Thread.objects.get(pk=thread_pk)
    quoted_post = Post.objects.get(id=post_pk)
    quote_content = quoted_post.content
    quote_sender = quoted_post.posted_by
    quote_timestamp = quoted_post.timestamp

    posts = Post.objects.filter(project=project, thread=thread).order_by('-timestamp')
    thread.last_posted = posts[0].timestamp
    thread.last_posted_by = user_member
    thread.save()

    if request.method == "POST":
        postform = PostForm(request.POST)
        post_content = postform.data['content']
        new_post = Post(posted_by=user_member, thread=thread, content=post_content, project=project, quote_content=quote_content, quote_sender=quote_sender, quote_timestamp=quote_timestamp, timestamp=datetime.now())
        new_post.save()
        thread.last_posted = datetime.now()
        thread.last_posted_by = user_member
        thread.save()
        return redirect('/project/' + pk + '/forum/' + thread_pk + '/view_thread/')
    else:
        postform = PostForm()

    context = {
        'project':project, 
        'members':members, 
        'user_member': user_member,
        'postform': postform, 
        'posts': posts,
        'thread': thread,
        'quoted_post':quoted_post,
    }
    return render(request, 'forum/thread.html', context)

