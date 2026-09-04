from rest_framework.serializers import ModelSerializer
from ..models import ExpenseSplit
from rest_framework import serializers

class ExpenseSplitSerializer(ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ["expense","user","amount"]
