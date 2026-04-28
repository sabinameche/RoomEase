from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
        path('signup/',views.RegisterView.as_view()),
        path('login/',views.LoginView.as_view()),

        path('group/',views.GroupView.as_view()),
        path('group/<int:id>/',views.GroupView.as_view()),

        path('group_invite/<int:id>/',views.GroupInvite.as_view()),
        path("invite/accept/<uuid:token>/", views.AcceptInvite.as_view()),
        path("invite/reject/<uuid:token>/", views.RejectInvite.as_view()),

        path('group_member/',views.GroupMemberView.as_view()),
        path('group_member/<int:id>/',views.GroupMemberView.as_view()),
]