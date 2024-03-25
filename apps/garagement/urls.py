from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.list_garages, name="garages"),
    path("<int:pk>/", views.get_garage, name="garage"),
    path("mine/", views.list_my_garages, name="my_garages"),
    path("create/", views.create_garage, name="create_garage"),
    path("images/create/", views.create_image, name="create_image"),
    path("images/", views.list_image, name="list_image"),
]
