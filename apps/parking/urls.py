from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("near/", views.get_parking_near, name="near"),
    path("create/", views.create_parking, name="create_parking"),
    path("getCreate/", views.create_parking_data, name="create_parking_get_data"),
    path("assign/<int:parking_id>", views.assign_parking, name="assign_parking"),
    path("transfer/<int:parking_id>", views.transfer_parking, name="transfer_parking"),
    path("delete/<int:parking_id>", views.delete_parking, name="delete_parking"),
    path("get_cities/<str:search_term>/", views.get_cities, name="get_cities"),
    path("<str:room_name>/", views.room, name="room"),
]