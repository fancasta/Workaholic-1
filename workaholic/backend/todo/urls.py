from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.todoPage, name="todoPage"),
    path('delete_todo/<str:todo_pk>/', views.deleteTodo, name="deleteTodo"),
    path('edit_todo/<str:todo_pk>/', views.editTodo, name="editTodo"),
]
