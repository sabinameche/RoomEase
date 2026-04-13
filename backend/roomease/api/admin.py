from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from api.models import (CustomUser)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username','profile_picture')