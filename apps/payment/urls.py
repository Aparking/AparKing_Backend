from django.urls import path

from . import views

urlpatterns = [
   # path("api/subscription/", views.create_subscription, name="create_subscription"),
    path('api/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('api/subscriptions/', views.getMembership, name='getMembership'),
    path('credits/', views.create_checkout_session_credit, name='create_checkout_session_credit')
]