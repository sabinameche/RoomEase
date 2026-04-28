from ..models import Group
from rest_framework import serializers
from .group_member_serializer import GroupMemberSerializer


class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True)
    class Meta:
        model = Group
        fields = ("id","name","currency","created_by","members")
        read_only_fields = ("id","member")

