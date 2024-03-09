from django.urls import path
from . import views

urlpatterns = [
    path('pricing-plan/', views.pricingPlan, name='pricingPlan'),
]