from rest_framework.serializers import ModelSerializer
from ..models import ExpenseSplit

class ExpenseSplitSerializer(ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ["expense","user","amount"]