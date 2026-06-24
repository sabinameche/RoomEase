from rest_framework.views import APIView
from rest_framework import serializers
from ..serializers_dir.expenseSplit_serializer import ExpenseSplitSerializer
from ..models import Group,ExpenseSplit,CustomUser,Expense
from rest_framework.response import Response
from django.db import transaction
from decimal import Decimal
from rest_framework import status

class ExpenseSplitView(APIView):
    def post(self,split_type,participants,expense):
        data = {}
        data["expense"] =expense

        if split_type == "EQUAL":
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                data["user"] = user
                data["amount"]=Decimal(expense.amount)/Decimal(len(participants))
                
                serializer = ExpenseSplitSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()


        elif split_type == "PERCENTAGE":
            total_percentage = sum((participants.values()))
    
            if total_percentage !=100:
                raise serializers.ValidationError("Percentage should be equal to 100")
            
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                data["user"] = user
                data["amount"]=(Decimal(participants[user_id]) * Decimal(expense.amount))/Decimal(100)
                
                serializer = ExpenseSplitSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

        elif split_type == "EXACT":
            for user_id in participants:
                user = CustomUser.objects.get(id = user_id)
                data["user"] = user
                data["amount"]=Decimal(participants[user_id])
                
                serializer = ExpenseSplitSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
        return serializer