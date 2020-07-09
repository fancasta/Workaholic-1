from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import *
from .forms import * 

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from datetime import datetime

from todo.models import Todo
from cal.models import Event

# Create your views here.

def registerPage(request):
    if request.method == 'POST':
        form = UserCreationForm_Edited(request.POST)        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email address taken!')
                form = UserCreationForm_Edited()
            else:
                #user = authenticate(username=username,password=password, email=email)                        
                #messages.success(request, 'Account was created successfully!')

                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False
                user.save()

                project_member = Project_Member(user=user)
                project_member.save()

                mail_subject = 'Activate your Workaholic account'
                current_site = get_current_site(request)
                message = render_to_string('accounts/acc_active_email.html', {
                    'user':user, 
                    'domain':current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                
                mail = EmailMessage(mail_subject, message, to=[email])
                mail.send(fail_silently=True)

                return redirect("login")
    else:        
        form = UserCreationForm_Edited()

    context = {
        'form' : form,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'accounts/register.html', context)

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return HttpResponse('Activation link is invalid!')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        try:
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect('index')
        except:
            messages.info(request,  'Invalid user. For new users, please activate your account through the link emailed to you.')

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')
    

@login_required(login_url='login')
def index(request):
    member = Project_Member.objects.get(user= request.user)
    projects = Project.objects.filter(project_members= member).order_by('-last_modified')

    project_notification = []
    number_of_notification = 0
    for project in projects:        
        todo = Todo.objects.filter(project=project)
        todo_list = []
        for i in todo:
            deadline = i.deadline.date()
            if deadline == datetime.today().date():
                todo_list.append(i)
                number_of_notification += 1

        events_start = Event.objects.filter(project=project)
        events_end = Event.objects.filter(project=project)

        events_start_list = []
        for i in events_start:
            if i.start_time and i.start_time.date() == datetime.today().date():
                events_start_list.append(i)
                number_of_notification += 1

        events_end_list = []
        for i in events_end:
            if i.end_time and i.end_time.date() == datetime.today().date():
                events_end_list.append(i)
                number_of_notification += 1

        project_notification.append([project, todo_list, events_start_list, events_end_list])

    context = {
        'projects':projects,
        'project_notification': project_notification,
        'number_of_notification': number_of_notification,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'accounts/index.html', context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm(request.POST)
    if request.method == "POST" and form.is_valid():
        project_name = form.cleaned_data['name']
        member = Project_Member.objects.get(user= request.user)
        project = Project(name=project_name, calendar_month=datetime.now(), last_modified=datetime.now(), last_modified_by=member)
        project.save()
        project.project_admin.add(request.user)
        project.project_members.add(member)
        return redirect('/')

    context = {
        'form':form,
        'Year': datetime.now().strftime("%Y")
    }
    return render(request, 'accounts/create_project.html', context)


