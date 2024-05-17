from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_booking, name='create_booking'),
    path('', views.list_my_bookings, name='list_my_bookings'),
    path('<int:pk>/', views.booking_details, name='booking_details'),
    path('create/', views.create_comment, name='create_comment'),
    path('createCheckoutSession/', views.create_checkout_session, name='create_checkout_session'),

]
