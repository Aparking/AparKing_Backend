from django.urls import path
from .views import create_claim, update_claim, delete_claim

urlpatterns = [
    path('claims/create/', create_claim, name='create_claim'),
    path('claims/update/<int:pk>/', update_claim, name='update_claim'),
    path('claims/delete/<int:pk>/', delete_claim, name='delete_claim'),
]