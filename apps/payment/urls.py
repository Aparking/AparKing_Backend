from django.urls import path
from . import views

urlpatterns = [
    path('pricingPlan/', views.pricingPlan, name='pricingPlan'),
]