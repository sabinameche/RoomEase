from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

# Register your models here.
from api.models import (CustomUser,Group,GroupInvite,GroupMember,Expense,ExpenseSplit,OwnedAmount)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id','username','profile_picture')

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ("id","name","currency","created_by")

@admin.register(GroupInvite)
class GroupInviteAdmin(ModelAdmin):
    list_display = ("email","token","status")

@admin.register(GroupMember)
class GroupMemberAdmin(ModelAdmin):
    list_display = ("id","user","role","group")

@admin.register(Expense)
class ExpenseAdmin(ModelAdmin):
    list_display = ('id','group','title','amount','paid_by','created_at','category','created_by')

@admin.register(ExpenseSplit)
class ExpenseSplitAdmin(ModelAdmin):
    list_display = ['expense','user','amount']

@admin.register(OwnedAmount)
class OwnedAmountAdmin(ModelAdmin):
    list_display = ['group','user','amount']
