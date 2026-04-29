from ..models import Group
from rest_framework import serializers
from .group_member_serializer import GroupMemberSerializer


class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True,read_only = True)
    currency = serializers.CharField(max_length=20,default = 'NPR')
    class Meta:
        model = Group
        fields = ("id","name","currency","created_by","members")
        read_only_fields = ("id","members")

