from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.todoPage, name="todoPage"),
    path('search_todo', views.searchTodo, name= "searchTodo"),
    path('delete_todo/<str:todo_pk>/', views.deleteTodo, name="deleteTodo"),
    path('edit_todo/<str:todo_pk>/', views.editTodo, name="editTodo"),
    path('up_todo/<str:todo_pk>/', views.upTodoRank, name="upTodo"),
    path('down_todo/<str:todo_pk>/', views.downTodoRank, name="downTodo"),
    path('view_todo/<str:todo_pk>/',views.viewTodo, name="viewTodo")
]