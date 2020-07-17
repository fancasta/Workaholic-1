from django.contrib import admin, auth
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.calendarPage, name="calendarPage"),
    path('search_event/', views.searchEvent, name='searchEvent'), #Why I can't move this path around?. If I move around, the link to search_event doesn't work and it always point to the calendarPage
    path('<str:action>/', views.calendarPage, name="calendarPage"),
    path('event/add_event/', views.editEvent, name="addEvent"),
    path('event/<str:event_id>/', views.viewEvent, name='viewEvent'),
    path('event/<str:event_id>/edit_event/', views.editEvent, name='editEvent'),
    path('event/<str:event_id>/delete_event/', views.deleteEvent, name='deleteEvent')
]