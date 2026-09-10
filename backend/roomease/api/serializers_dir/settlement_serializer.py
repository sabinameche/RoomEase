from rest_framework.serializers import ModelSerializer
from ..models import Settlement
class SettlementSerializer(ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['group','settled_by','received_by','amount','created_at']
    