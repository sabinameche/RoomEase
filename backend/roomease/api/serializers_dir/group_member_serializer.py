from rest_framework import serializers
from ..models import GroupMember

class GroupMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    user_id = serializers.IntegerField(source= "user.id")
    class Meta:
        model = GroupMember
        fields=["id","user","group","role","username","user_id"]
        read_only_fields = ["id"]