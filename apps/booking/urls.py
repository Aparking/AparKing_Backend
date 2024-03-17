from django.urls import path
from . import views

urlpatterns = [
    path('claims/', views.ClaimAdminListAPIView.as_view(), name='claims-admin'),
]
