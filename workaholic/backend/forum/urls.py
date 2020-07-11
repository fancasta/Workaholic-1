from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.forumPage, name="forum"),
    path('<str:thread_pk>/view_thread/', views.threadPage, name="thread"),
    path('<str:thread_pk>/delete_thread/', views.deleteThread, name="delete_thread"),
    path('<str:thread_pk>/edit_thread/', views.editThread, name="edit_thread"),

    path('<str:thread_pk>/edit_post/<str:post_pk>/', views.editPost, name="edit_post"),
    path('<str:thread_pk>/delete_post/<str:post_pk>/', views.deletePost, name="delete_post"),
    path('<str:thread_pk>/quote_post/<str:post_pk>/', views.quotePost, name="quote_post")
]
