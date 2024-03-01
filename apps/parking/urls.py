from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("near/", views.get_parking_near, name="near"),
    path("create/", views.create_parking, name="create_parking"),
    path("<str:room_name>/", views.room, name="room"),
]