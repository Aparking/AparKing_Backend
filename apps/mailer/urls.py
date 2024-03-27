from django.urls import path, include
from .views import send_email


urlpatterns = [
    path('', send_email, name='email'),
    path('send_email/', send_email, name='send_email'),
]
