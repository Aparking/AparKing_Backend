from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
    path('verify/', views.verify_user, name='verify'),
    path('deleteAccount/', views.delete_account, name='deleteAccount'),
]