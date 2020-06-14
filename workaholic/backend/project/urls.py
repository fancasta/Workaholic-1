from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('<str:pk>/', views.projectPage, name="projectPage"),
    
    path('<str:pk>/delete_member/<str:member_pk>/', views.deleteMember, name="deleteMember"),
    path('<str:pk>/chat/', include('chat.urls')),

    path('<str:pk>/todo/', include('todo.urls')),
    path('<str:pk>/board/', include('board.urls')),
    path('<str:pk>/calendar/', include('cal.urls')),
    path('<str:pk>/delete_project/', views.deleteProject, name="deleteProject")
]
