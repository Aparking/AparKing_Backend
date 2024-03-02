from django.urls import path
from . import views

urlpatterns = [
    path('garages/', views.GarageListCreateAPIView.as_view(), name='garages'),
    path('garages/images/', views.ImageListCreateAPIView.as_view(), name='garages-images'),
    path('garages/availability/', views.AvailabilityListCreateAPIView.as_view(), name='garages-available'),

]