from rest_framework import serializers
from ..models import GroupMember

class GroupMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    class Meta:
        model = GroupMember
        fields=["user","group","role","username"]