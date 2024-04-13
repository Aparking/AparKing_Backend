from django.urls import path
from . import views

urlpatterns = [
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/', views.list_my_bookings, name='list_my_bookings'),
    path('bookings/<int:pk>/', views.booking_details, name='booking_details'),
    path('bookings/create-checkout-session/', views.create_checkout_session, name='create_checkout_session')
]