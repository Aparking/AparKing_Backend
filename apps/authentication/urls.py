from django.urls import path
from django.shortcuts import render

from . import views
# Create your views here.


urlpatterns = [
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
    path('api/users', views.users_list),
    path('api/users/<int:pk>/', views.users_detail)
]