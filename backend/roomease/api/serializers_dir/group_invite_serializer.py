from rest_framework import serializers
from ..models import GroupInvite

class GroupInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupInvite
        fields = ("email","group","invited_by")