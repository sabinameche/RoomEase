from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

# Register your models here.
from api.models import (CustomUser,Group,GroupInvite,GroupMember)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username','profile_picture')

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ("id","name","currency","created_by")

@admin.register(GroupInvite)
class GroupInviteAdmin(ModelAdmin):
    list_display = ("email","token","status")

@admin.register(GroupMember)
class GroupMemberAdmin(ModelAdmin):
    list_display = ("user","role","group")