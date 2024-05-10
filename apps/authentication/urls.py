<<<<<<< HEAD
from django.urls import path
from . import views
# Create your views here.


urlpatterns = [
    path('login/', views.auth_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.auth_logout, name='logout'),
    path('api/users', views.users_list),
    path('api/users/<int:pk>/', views.users_detail)
=======
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
    path("user/profile/", views.user_profile, name="user-profile"),
>>>>>>> f293d260ec4089ef07c2cc253cf94d8acfe4bc48
]