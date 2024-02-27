from django.contrib import admin
from .models import BaseUser, AparkingUser
# Register your models here.
admin.site.register(BaseUser)
admin.site.register(AparkingUser)