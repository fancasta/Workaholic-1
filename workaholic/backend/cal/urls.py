from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.calendarPage, name="calendarPage"),
    path('<str:action>/', views.calendarPage, name="calendarPage"),
    path('event/add_event/', views.event, name="addEvent"),
    path('event/<str:event_id>/', views.event, name='event_edit'),
    path('event/<str:event_id>/delete_event/', views.deleteEvent, name='deleteEvent')
]
