from django.urls import path
from . import views

urlpatterns = [
    path('garages/', views.GarageListCreateAPIView.as_view(), name='garages'),
    path('garages/<int:pk>/', views.GarageRetrieveUpdateDestroyAPIView.as_view(), name='garage-detail'),
    path('garages/images/', views.ImageListCreateAPIView.as_view(), name='garages-images'),
    path('garages/images/<int:pk>/', views.ImageRetrieveUpdateDestroyAPIView.as_view(), name='garages-images-detail'),
    path('garages/availability/', views.AvailabilityListCreateAPIView.as_view(), name='garages-available'),
    path('garages/availability/<int:pk>/', views.AvailabilityRetrieveUpdateDestroyAPIView.as_view(), name='garages-available-detail'),
]