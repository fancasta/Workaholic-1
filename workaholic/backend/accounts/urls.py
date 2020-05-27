from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/register/', views.registerPage, name='register'),
    path('accounts/login/', views.loginPage, name="login"),
    path('accounts/logout/', views.logoutPage, name="logout"),
    path('accounts/createProject/', views.createProject, name="createProject")
]
