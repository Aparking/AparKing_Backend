from django.urls import path
from . import views

urlpatterns = [
    # path('garages/', views.GarageListCreateAPIView.as_view(), name='garages'),
    # path('garages/<int:pk>/', views.GarageRetrieveUpdateDestroyAPIView.as_view(), name='garage-detail'),
    # path('garages/images/', views.ImageListCreateAPIView.as_view(), name='garages-images'),
    # path('garages/images/<int:pk>/', views.ImageRetrieveUpdateDestroyAPIView.as_view(), name='garages-images-detail'),
    # path('garages/availability/', views.AvailabilityListCreateAPIView.as_view(), name='garages-available'),
    # path('garages/availability/<int:pk>/', views.AvailabilityRetrieveUpdateDestroyAPIView.as_view(), name='garages-available-detail'),
    # path('garages/available/', views.AvailableGaragesListAPIView.as_view(), name='available-garages'),
    # path('garages/mine/', views.MyGaragesListAPIView.as_view(), name='my-garages'),
    # path('garages/mine/available/', views.MyAvailableGaragesListAPIView.as_view(), name='my-available-garages'),
    path(
        "garages/",
        views.GarageViewSet.as_view({"get": "listGarages", "post": "create"}),
        name="garages",
    ),
    path(
        "garages/<int:pk>/",
        views.GarageViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="garage-detail",
    ),
]