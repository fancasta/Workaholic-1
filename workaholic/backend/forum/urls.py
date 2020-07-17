from django.contrib import admin, auth
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.forumPage, name="forum"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('<str:thread_pk>/view_thread/', views.threadPage, name="thread"),
    path('<str:thread_pk>/delete_thread/', views.deleteThread, name="delete_thread"),
    path('<str:thread_pk>/edit_thread/', views.editThread, name="edit_thread"),

    path('<str:thread_pk>/edit_post/<str:post_pk>/', views.editPost, name="edit_post"),
    path('<str:thread_pk>/delete_post/<str:post_pk>/', views.deletePost, name="delete_post"),
    path('<str:thread_pk>/quote_post/<str:post_pk>/', views.quotePost, name="quote_post"),
    path('<str:thread_pk>/like_post/<str:post_pk>/', views.likePost, name="like_post"),
    path('<str:thread_pk>/dislike_post/<str:post_pk>/', views.dislikePost, name="dislike_post")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
