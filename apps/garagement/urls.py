from django.urls import path
from . import views

urlpatterns = [
    path('garages/', views.list_garages, name='garages'),
    path('garages/mine', views.list_my_garages, name='my_garages'),
    path('garages/create/', views.create_garage, name='create_garage'),
    path('garages/images/create/', views.create_image, name='create_image'),
    path('garages/images/', views.list_image, name='list_image'),
]