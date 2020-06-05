from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:pk>/', views.projectPage, name="projectPage"),
    path('<str:pk>/add_members/', views.addMembers, name="addMembers"),
    
    path('<str:pk>/delete_member/<str:member_pk>/', views.deleteMember, name="deleteMember"),
    path('<str:pk>/chat/', include('chat.urls')),

    path('<str:pk>/todo/', include('todo.urls'))


]
