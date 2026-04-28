from django.shortcuts import render

# Create your views here.
from .views_dir import register_view,group_view,group_invite_view,group_member_view

RegisterView = register_view.RegisterView
LoginView = register_view.LoginView

GroupView = group_view.GroupView

AcceptInvite = group_invite_view.AcceptInvite
RejectInvite = group_invite_view.RejectInvite
GroupInvite = group_invite_view.GroupInviteView

GroupMemberView = group_member_view.GroupMemberView