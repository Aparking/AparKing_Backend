from django.urls import path
from django.shortcuts import render

from . import views
# Create your views here.


urlpatterns = [
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
      path('api/users', views.users_list),
    #path(r'^api/users/(?P<pk>[0-9]+)$', views.users_detail),
]