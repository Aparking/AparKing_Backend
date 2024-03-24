from django.urls import path

from . import views

urlpatterns = [
    path("api/subscription/", views.create_subscription, name="create_subscription"),
]