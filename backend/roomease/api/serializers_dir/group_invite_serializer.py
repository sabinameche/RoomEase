from rest_framework import serializers
from ..models import GroupInvite

class GroupInviteSerializer(serializers.ModelSerializer):
    email = serializers.ListField(child = serializers.EmailField(),required = False)
    class Meta:
        model = GroupInvite
        fields = ("email","group","invited_by")