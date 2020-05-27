from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('home/<str:pk>/', views.projectPage, name="projectPage")
]
