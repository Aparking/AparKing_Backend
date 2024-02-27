from django.urls import path
from . import views

urlpatterns = [
    path('', views.app, name='app'),
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
]