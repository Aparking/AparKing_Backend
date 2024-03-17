from django.urls import path
from .views import create_claim

urlpatterns = [
    path('claims/create/', create_claim, name='create_claim'),
]