from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.auth_login, name="login"),
    path("register/", views.register, name="register"),
    path("registerVehicle/", views.registerVehicle, name="registerVehicle"),
    path("logout/", views.auth_logout, name="logout"),
    path("verify/", views.verify_user, name="verify"),
    path("deleteAccount/", views.delete_account, name="deleteAccount"),
    path("user-info/", views.user_info, name="userInfo"),
    path("updateVehicle/", views.updateVehicle, name="updateVehicle"),
]