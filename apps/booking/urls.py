from django.urls import path
from . import views

urlpatterns = [
    path('comments/create/', views.create_comment, name='create_comment'),
]