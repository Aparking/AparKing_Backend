from django.urls import path
from . import views

urlpatterns = [
    path('garages/', views.list_garage, name='garages'),
    path('garages/create/', views.create_garage, name='create_garage'),
    path('garages/images/create/', views.create_image, name='create_image'),
    path('garages/images/', views.list_image, name='list_image'),
]